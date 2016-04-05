"""tracking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from report.views import (report_monthly, report_monthly_view, report_days_view, report_year_view,
    report_url_domain, dashboard_user, report_campaign_view, report_campaign_year_view,
    report_campaign_month_view, report_campaign_day_view, report_url_day_view)

urlpatterns = [
    url(r'^url/by/month/json/$', report_monthly),
    url(r'^url/by/month/$', report_monthly_view),
    url(r'^url/by/days/$', report_days_view),
    url(r'^url/by/year/$', report_year_view),
    url(r'^url/by/hour/$', report_url_day_view),
    url(r'^url/by/domain/$', report_url_domain),
    url(r'^url/by/campaign/$', report_campaign_view),
    url(r'^url/by/campaign/year/$', report_campaign_year_view),
    url(r'^url/by/campaign/month/$', report_campaign_month_view),
    url(r'^url/by/campaign/day/$', report_campaign_day_view),
    url(r'^$', dashboard_user),
]
