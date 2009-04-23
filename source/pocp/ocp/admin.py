#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

from pocp.ocp.models import active_route, active_conf, provider, round_robin, user_agent
from django.contrib import admin

admin.site.register(active_route)
admin.site.register(active_conf)
admin.site.register(provider)
admin.site.register(round_robin)
admin.site.register(user_agent)

