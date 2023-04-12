from django.http import JsonResponse, HttpResponse
from django.views import View
import django
import sys
import os
sys.path.append('C:\\Users\\shahid awan\\restaurantapi')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurantapi.settings")
django.setup()
from restaurantapi.utils import get_report_csv, get_report_status,trigger_report_generation

class TriggerReportView(View):
    def get(self, request):
        report_id = trigger_report_generation()
        return JsonResponse({'report_id': report_id})

class GetReportView(View):
    def get(self, request):
        print(str(request))
        report_id = request.GET['report_id']
        status, csv_file_path = get_report_status(report_id)
        if status == 'Complete':
            return get_report_csv(report_id, csv_file_path)
        else:
            return JsonResponse({'status': status})