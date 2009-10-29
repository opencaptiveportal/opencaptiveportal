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

    # Static css and image stuff
    # Change the directory to an absolute directory
    (r'^rsc/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': '/usr/local/pocp/templates/rsc/'}),

    # Landingpage:
    (r'^/*back.php',            'pocp.ocp.views.back'),
    (r'^/*route.php',           'pocp.ocp.views.route'),
    (r'^/*index.php',           'pocp.ocp.views.landingpage'),
    (r'^/*pwlan/+back.php',     'pocp.ocp.views.back'),
    (r'^/*pwlan/+route.php',    'pocp.ocp.views.route'),
    (r'^/*pwlan/+index.php',    'pocp.ocp.views.landingpage'),

    (r'^service/iptables/show',    'pocp.ocp.view_iptables.show'),
    (r'^service/iptables/rebuild', 'pocp.ocp.view_iptables.rebuild'),
    
    (r'^service/ip/show',          'pocp.ocp.view_ip.show'),
    (r'^service/ip/rebuild',       'pocp.ocp.view_ip.rebuild'),

    (r'^provider/dhcp.php',        'pocp.ocp.provider.dhcp'),

    (r'^admin-overview/',       'pocp.ocp.views.admin'),


    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/(.*)', admin.site.root),

    (r'^login/$',   'django.contrib.auth.views.login', {'template_name': 'login.htm'}),
    (r'',           'pocp.ocp.views.landingpage'),
)
