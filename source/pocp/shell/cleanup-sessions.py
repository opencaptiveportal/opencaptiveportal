#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Clean up old sessions

import sys
sys.path.append("../../")

from pocp.settings_xml_rpc import LEASE_FILE
from pocp.helper.dhcpd import parse_lease_file
from pocp.ocp.models import active_route, active_conf

# 1)  Clear seassions
#     Normally, this should be done with django-admin.py cleanup, but this does
#     not work (why?)
#     Therefore, delete the entries in the database table
#     pocp=> DELETE FROM django_session where expire_date >= now();

from django.core.management import setup_environ
import pocp.settings 
setup_environ(pocp.settings)
from django.contrib.sessions.models import Session
import datetime
from django.db import transaction

Session.objects.filter(expire_date__lt=datetime.datetime.now()).delete()
transaction.commit_unless_managed()

# 2)  Delete ldap users
#     If a users authenticates via ldap, da django user is created.  Delete
#     these users once in a while, because they just consume database space.
# 
#     Delete all users with group ldap and a last_login smaller than 7 days before
#     SELECT * from auth_user_groups u join auth_group g on (u.group_id = g.id) where g.name = 'ldap';

from django.contrib.auth.models import User, Group
User.objects.filter( groups__name = "ldap", last_login__lt = datetime.datetime.now() - datetime.timedelta( 7 ) ).delete()

