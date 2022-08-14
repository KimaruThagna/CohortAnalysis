import pandas as pd
import datetime
import random

start_date = datetime.date(2020, 1, 1)
end_date = datetime.date(2020, 2, 1)
SUBSCRIPTION_PLAN=["Monthly", "Annually"]
CUSTOMER_ORIGIN = ["Organic", "Ads"]

def random_date(start_date, end_date, offset=0):
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    return start_date + datetime.timedelta(days=random_number_of_days+offset)




