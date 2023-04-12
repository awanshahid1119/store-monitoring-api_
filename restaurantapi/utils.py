import os
import random
import string
from django.http import HttpResponse
#######################################


from datetime import datetime, timedelta
from django.db.models import Count, Max, Q, Sum
from pytz import timezone
# from restaurantapi.models import StoreActivity, BusinessHours, StoreTimeZone

######################################
import pandas as pd
import math
import pytz
from datetime import datetime, timedelta
from django.conf import settings
import django
import sys
sys.path.append('C:\\Users\\shahid awan\\restaurantapi')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurantapi.settings")
django.setup()
from restaurantapi.models import StoreActivity, BusinessHours, StoreTimeZone

def trigger_report_generation():
    report_id = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    compute_report(report_id)
    return report_id

def compute_report(report_id):
    # Load data from the models
    store_activities = StoreActivity.objects.all()
    business_hours = BusinessHours.objects.all()
    store_timezones = StoreTimeZone.objects.all()

    # Preprocess the data
    store_activities_df = pd.DataFrame(list(store_activities.values()))
    business_hours_df = pd.DataFrame(list(business_hours.values()))
    store_timezones_df = pd.DataFrame(list(store_timezones.values()))

    # Merge data sources
    # print(business_hours)
    merged_data = store_activities_df.merge(store_timezones_df, on='store_id', how='left')
    print('here mothafucka')
    merged_data = merged_data.merge(business_hours_df, on='store_id', how='left')
    merged_data = merged_data[:10]
    
    # print(merged_data)
    # Convert timestamp_utc to local time
    merged_data['timestamp_local'] = merged_data.apply(lambda x: x['timestamp_utc'].tz_localize(pytz.timezone(x['timezone_str'] if not pd.isna(x['timezone_str']) else 'America/Chicago')), axis=1)
    
    # Compute the uptime and downtime
    report_data = compute_uptime_downtime(merged_data)
    
    # Save the final report DataFrame as a CSV file
    csv_file_path = os.path.join(settings.MEDIA_ROOT, f'report_{report_id}.csv')
   
    report_data.to_csv(csv_file_path, index=False)
   

def compute_uptime_downtime(merged_data):
    report_data = pd.DataFrame(columns=['store_id', 'uptime_last_hour', 'uptime_last_day', 'uptime_last_week',
                                        'downtime_last_hour', 'downtime_last_day', 'downtime_last_week'])

    for store_id in merged_data['store_id'].unique():
        store_data = merged_data[merged_data['store_id'] == store_id].copy()

        # Get the first and last timestamps for the store data
        min_ts = store_data['timestamp_local'].min()
        max_ts = store_data['timestamp_local'].max()

        # Define the time ranges for the metrics
        last_hour_range = (max_ts - timedelta(hours=1), max_ts)
        last_day_range = (max_ts - timedelta(days=1), max_ts)
        last_week_range = (max_ts - timedelta(weeks=1), max_ts)

        # Compute uptime and downtime for each time range
        uptime_last_hour, downtime_last_hour = compute_uptime_downtime_range(store_data, last_hour_range)
        uptime_last_day, downtime_last_day = compute_uptime_downtime_range(store_data, last_day_range)
        uptime_last_week, downtime_last_week = compute_uptime_downtime_range(store_data, last_week_range)

        # Add the metrics to the report data
        row_data = {
            'store_id': store_id,
            'uptime_last_hour': uptime_last_hour,
            'uptime_last_day': uptime_last_day,
            'uptime_last_week': uptime_last_week,
            'downtime_last_hour': downtime_last_hour,
            'downtime_last_day': downtime_last_day,
            'downtime_last_week': downtime_last_week
        }

        report_data = pd.concat([report_data, pd.DataFrame(row_data, index=[0])], ignore_index=True)

    return report_data

def compute_uptime_downtime_range(store_data, time_range):
    # Filter the store data to the specified time range
    range_data = store_data[(store_data['timestamp_local'] >= time_range[0]) &
                            (store_data['timestamp_local'] < time_range[1])]

    # Compute the total number of polls and the number of successful polls in the range
    total_polls = len(range_data)
    success_polls = len(range_data[range_data['status'] == 'success'])

    # Compute uptime and downtime percentages
    uptime = 100 * success_polls / total_polls if total_polls > 0 else 0
    downtime = 100 - uptime

    return uptime, downtime

def get_report_status(report_id):
    csv_file_path = os.path.join(settings.MEDIA_ROOT, f'report_{report_id}.csv')
    if os.path.exists(csv_file_path):
        return "Complete", csv_file_path
    else:
        return "Running", None

def get_report_csv(report_id, csv_file_path):
    with open(csv_file_path, 'rb') as csv_file:
        response = HttpResponse(csv_file.read(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="report_{report_id}.csv"'
        return response