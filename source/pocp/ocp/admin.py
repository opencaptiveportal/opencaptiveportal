#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

from pocp.ocp.models import active_route, provider
from django.contrib import admin

admin.site.register(active_route)
admin.site.register(provider)

