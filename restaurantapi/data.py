# load_data.py
import pandas as pd
import os
import django
import sys
sys.path.append('C:\\Users\\shahid awan\\restaurantapi')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurantapi.settings")
django.setup()
from restaurantapi.models import StoreActivity, BusinessHours, StoreTimeZone


def load_data():
    activity_df = pd.read_csv("restaurantapi/activity.csv")
    business_hours_df = pd.read_csv("restaurantapi/business_hours.csv")
    timezone_df = pd.read_csv("restaurantapi/timezones.csv")

    activity_list  = []
    business_list = []
    timezone_list = []

    # Load data into StoreActivity model
    ctr = 0
    print(ctr)
    for _, row in activity_df.iterrows():
        timestamp=row['timestamp_utc']
        splits=timestamp.rsplit(' ')
        timestamp = splits[0]+' '+splits[1]
        activity_list.append(StoreActivity(store_id=row['store_id'], timestamp_utc=timestamp, status=row['status']))

    # Load data into BusinessHours model
    for _, row in business_hours_df.iterrows():
        business_list.append(BusinessHours(store_id=row['store_id'], day_of_week=row['day'], start_time_local=row['start_time_local'], end_time_local=row['end_time_local']))

    # Load data into StoreTimeZone model
    for _, row in timezone_df.iterrows():
        timezone_list.append(StoreTimeZone(store_id=row['store_id'], timezone_str=row['timezone_str']))

    StoreActivity.objects.bulk_create(activity_list)

    BusinessHours.objects.bulk_create(business_list)

    StoreTimeZone.objects.bulk_create(timezone_list)

if __name__ =='__main__':
    load_data()