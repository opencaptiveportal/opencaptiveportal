#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^pocp/', include('pocp.foo.urls')),

    # landingpage:
    (r'^back.php',  'pocp.ocp.views.back'),
    (r'^route.php', 'pocp.ocp.views.route'),
    (r'^index.php', 'pocp.ocp.views.landingpage'),


    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    (r'^login/$',   'django.contrib.auth.views.login', {'template_name': 'login.htm'}),
#    (r'',           'django.contrib.auth.views.login', {'template_name': 'landingpage.htm'}),
    (r'',           'pocp.ocp.views.landingpage'),
)
