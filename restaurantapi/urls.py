"""
URL configuration for restaurantapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
import django
import sys
sys.path.append('C:\\Users\\shahid awan\\restaurantapi')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurantapi.settings")
django.setup()
from django.contrib import admin
from django.urls import path
import restaurantapi.views  as views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('TriggerReportView/', views.TriggerReportView.as_view(),name='trigger'),
    path('GetReportView/', views.GetReportView.as_view(),name='getreport'),
         
]
