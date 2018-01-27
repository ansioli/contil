from django.conf.urls import patterns, include, url
from boletos.views import *

urlpatterns = patterns('',
    url(r'^login/$', 'boletos.views.login' , name="login"),
    url(r'^home/$', 'boletos.views.home' , name="home"),
    url(r'^bloco/$', 'boletos.views.bloco' , name="bloco"),

)
