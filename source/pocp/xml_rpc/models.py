#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class xml_rpc_server(models.Model):
  class Meta:
    permissions = (('xml_rpc', "Is allowed to log into XML-RPC"), )

class handle(models.Model):
  user      = models.ForeignKey(User)
  handle    = models.CharField(max_length=255, unique = True)
  last_seen = models.DateTimeField(auto_now_add=True) 

  def __str__(self):
    return "Secret handle from user %s" % (str(self.user))

  class Admin:
    list_display  = ('user', 'handle', 'last_seen')
    search_fields = ['user']

