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
from track.views import generate_id, test_1, test_2, save_data, login_view, logout_view

urlpatterns = [
    url(r'^assign_id/', generate_id),
    url(r'^save_data/', save_data),
    url(r'^login/', login_view, name="login"),
    url(r'^logout/', logout_view, name="logout"),
    url(r'^test1/', test_1),
    url(r'^test2/', test_2),    
]
