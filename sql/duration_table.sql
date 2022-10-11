-- To build a duration table, we define a censoring date(cut off point of the analysis)
-- can be arbitrary date or maximum date in your dataset.
-- We then calulate duration from start date to EITHER end date where target action happens or censoring date in case action does not happen
{% set censoring_time_query %}
SELECT MAX(EventDate) AS CensorDate FROM {{ref('events')}}
{% endset %}

{% set censoring_time = run_query(censoring_time_query) %}
{% if execute %}
-- Return the date
{% set max_date = censoring_time.columns[0].values()[0] %}
{% else %}
{% set max_date = [] %}
{% endif %}

WITH user_start_dates AS
(
    SELECT UserId, RegistrationDate
    FROM {{ref('users')}}
)

-- find out the first SYSTEM ERROR event per user. Remember our goal is assessing how long until FIRST error occurs
, first_occurence_of_target_event AS (
 SELECT 
        *
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER(PARTITION BY UserId ORDER BY EventDate ASC) AS row_num
        FROM {{ref('events')}} WHERE EventType = 'SYSTEM ERROR'
    ) AS _
    WHERE row_num = 1
)

, final AS (
SELECT 
users.UserId, users.RegistrationDate, target_events.EventType,
DATEDIFF(DAY,  users.RegistrationDate , COALESCE(target_events.EventDate, CAST('{{max_date}}' AS DATE) ) ) AS days_to_event
FROM user_start_dates as users LEFT JOIN first_occurence_of_target_event as target_events
ON users.UserId = target_events.UserId
)
SELECT * FROM final WHERE days_to_event > 0
