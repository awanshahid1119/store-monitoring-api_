
#admin
from django.contrib import admin
from .models import StoreActivity 
from .models import BusinessHours
from .models import StoreTimeZone

admin.site.register(StoreActivity)
admin.site.register(BusinessHours)
admin.site.register(StoreTimeZone)