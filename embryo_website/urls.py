"""embryo_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

import os
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import *

# Custom IMPORTS
from embryo_website import settings
# from embryo_website.views import *
import admin_tools

admin.autodiscover()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    path('tinymce/', include('tinymce.urls')),
 #    path('', writeup, {}),
 #    path('apogee_innovation_challenge/', aic),
 #    path('tracks/(\d+)/', aic_track),
 #    path('company_details/(\d+)/', company_details),
 #    path('company_register/(\d+)/', company_register),
 #    path('company_upload/(\d+)/', company_upload),
 #    path('company_thank_you/(\d+)/', company_thank_you),
 #    path('testsuccess/',get_from_mail),
 #    path('success/',redirect),
 #    path('lecturedetail_id=(\d+)/', lecturedetail),
 #    path('event_id=(\d+)/',event),
 #    path('lectures/', lectures),
 #    path('lectures/(\d+)/', lectures),
	# path('atmos/detail/(\d+)/', atmosdetail),
	# path('atmos/lectures/(\d+)/', atmos_list),
 #    path('gallery/', gallery),
 #    path('newsletters/', newsletters),
 #    path('discipline',discipline),
 #    path('register/', register),
 #    path('eventregister/', eventregister),
 #    path('eventthankyou/', art_success),
	# path('search_result',searching),
 #    path('php', redirector),
 #    path('faculty/', rohan),
 #    path('site_media/(?P<path>.*)', 'django.views.static.serve',  {'document_root': settings.MEDIA_ROOT}),
 #    path('(?P<name>[-\w]+)/', writeup, {}),
]

