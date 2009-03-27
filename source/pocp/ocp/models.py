#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

from django.db import models

# Create your models here.

class active_route(models.Model):
    src_ip      = models.IPAddressField(unique=True)
    provider    = models.ForeignKey('provider')

    def __str__(self):
        return "%s via %s" % (self.src_ip, self.provider.name)

    class Admin:
        list_display  = ('src_ip', 'provider')
        search_fields = ['src_ip']

class provider(models.Model):
    name        = models.CharField(max_length=255)
    gre_tunnel  = models.IntegerField()
    local_ipv4  = models.IPAddressField()   # GRE tunnel endpoints
    remote_ipv4 = models.IPAddressField()
    int_ipv4    = models.IPAddressField()   # interface IP Address
    int_ipv6    = models.IPAddressField()   # interface IP Address

    def __str__(self):
        return str(self.name)

    class Admin:
        list_display  = ('name', 'gre_tunnel')
        search_fields = ['name']

