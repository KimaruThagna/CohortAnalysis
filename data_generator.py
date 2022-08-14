import pandas as pd
import datetime
import random

start_date = datetime.date(2021, 1, 1)
end_date = datetime.date(2021, 12, 31)

SUBSCRIPTION_PLAN=["Economy Pack", "Advanced Pack"]
CUSTOMER_ORIGIN = ["Organic", "Ads"]
EVENT_TYPE=["SYSTEM ERROR", "ROUTINE CHECK"]
COUNTRY = ["KE","UG","NG","AU","US","UK"]
USER_COLUMNS = ["UserId","RegistrationDate",
"Country","UserOrigin","SubscriptionPlan" ]
EVENT_COLUMNS=["UserId", "SubscriptionPlan", "EventDate", "EventType", "EventId"]

# generate random date in YYYYMMDD format
def random_date(start_date, end_date):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_number_of_days)


def generate_synthetic_data(counter):
    user_id = counter
    subscription = SUBSCRIPTION_PLAN[random.randrange(0,2)]
    customer_origin = CUSTOMER_ORIGIN[random.randrange(0,2)]
    registration_date = random_date(start_date,end_date)
    country = COUNTRY[random.randrange(0,5)]
    event_id = random.randrange(1000000000,1000000000000000)
    user_foreign_key = random.randrange(100) # limiting to 10% of set to allow repetition
    event_type = EVENT_TYPE[random.randrange(0,2)]
    event_date = random_date(registration_date,end_date) # events occur after start date
    event_sub_plan = subscription
    # create a list of random records generated
    user_record = [user_id, registration_date, country, customer_origin, subscription]
    event_record = [user_foreign_key, event_sub_plan, event_date, event_type, event_id]
    return user_record, event_record

# generate CSV file with records
user_records = []
event_records = []
for i in range(1000):
    user, event = generate_synthetic_data(i)
    user_records.append(user)
    event_records.append(event)

users = pd.DataFrame(user_records, columns=USER_COLUMNS)
events = pd.DataFrame(event_records, columns=EVENT_COLUMNS)
users.to_csv('data/users.csv')
events.to_csv('data/events.csv')




