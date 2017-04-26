"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth import views
#import myproject.poster.urls
# from myproject.poster import * 
# from myproject.approver.urls import *
admin.autodiscover()
urlpatterns = [
	url(r'^post/',include('poster.urls')),
	url(r'^$',include('poster.urls')),
	url(r'^approve/',include('approver.urls')),
	url(r'^admin/',include(admin.site.urls)),
	url(r'^login',views.login,{'template_name':'login.html'}),
	url(r'^logout',views.logout),
	]
