from django.conf.urls import patterns, include, url
from django.contrib import admin
from boletos.views import *


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('boletos.urls')),
)
