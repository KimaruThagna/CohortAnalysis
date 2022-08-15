
-- To build a duration table, we define a censoring date(cut off point of the analysis)
-- can be arbitrary date or maximum date in your dataset.
-- We then calulate duration from start date to EITHER end date where target action happens or censoring date in case action does not happen

WITH user_start_dates AS
(
    SELECT UserId, RegistrationDate
    FROM {{ref('users')}}
)
, censoring_time AS (
    SELECT MAX(EventDate) FROM {{ref('events')}}
)
-- find out the first SYSTEM ERROR event per user. Remember our goal is assessing how long until FIRST error occurs
, first_occurence_of_target_event AS (
 SELECT 
        *
    FROM (
        SELECT
            *,
            ROW_NUMBER() OVER(PARTITION BY visitorid ORDER BY event_at ASC) AS row_num
        FROM {{ref('events')}} WHERE EventType = 'SYSTEM ERROR'
    ) AS _
    WHERE row_num = 1
)

, final AS (
SELECT 
users.UserId, users.RegistrationDate, target_events.EventType, 
COALESCE(target_events.EventDate, censoring.EventDate) - users.RegistrationDate as duration
FROM user_start_dates as users, censoring LEFT JOIN first_occurence_of_target_event as target_events
ON users.UserId = target_events.UserId
)
SELECT * FROM first_occurence_of_target_event
