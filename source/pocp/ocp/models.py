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

    def save(self, force_insert=False, force_update=False):
        from pocp.helper.iptables import insert_route
        # Insert route in iptables, if fail -> exception
        insert_route(self.src_ip, str(self.provider.gre_tunnel))
        super(active_route, self).save(force_insert, force_update) # Call the "real" save() method.

    def delete(self):
        from pocp.helper.iptables import delete_route
        # and then in iptables
        delete_route(self.src_ip)
        super(active_route, self).delete() # Call the "real" save() method.


class active_conf(models.Model):
    src_ip      = models.IPAddressField(unique=True)

    def __str__(self):
        return "%s" % (self.src_ip)

    class Admin:
        list_display  = ('src_ip')
        search_fields = ['src_ip']

    def save(self, force_insert=False, force_update=False):
        from pocp.helper.iptables import insert_conf
        # Insert route in iptables, if fail -> exception
        insert_conf(self.src_ip)
        super(active_conf, self).save(force_insert, force_update) # Call the "real" save() method.

    def delete(self):
        from pocp.helper.iptables import delete_conf
        # and then in iptables
        delete_route(self.src_ip)
        super(active_conf, self).delete() # Call the "real" save() method.


class provider(models.Model):
    name        = models.CharField(max_length=255, unique=True)
    gre_tunnel  = models.IntegerField()
    local_ipv4  = models.IPAddressField()   # GRE tunnel endpoints
    remote_ipv4 = models.IPAddressField()
    int_ipv4    = models.IPAddressField()   # interface IP Address
    int_ipv6    = models.IPAddressField()   # interface IP Address
    user_agent  = models.ManyToManyField("user_agent", blank=True)
    iframe_url  = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Admin:
        list_display  = ('name', 'gre_tunnel')
        search_fields = ['name']


# TODO: online eine liste mir den daten haben und die dann wie die
# SWITCHclassic ACLs holen
class round_robin(models.Model):
    provider    = models.ForeignKey('provider', unique=True)
    rate        = models.FloatField()   # TODO: check, that rate in [0,1] and sum(rate) = 1

    def __str__(self):
        return str("%0.2f (%02.f%%) %s" % (self.rate, self.rate*100, self.provider.name))

    class Admin:
        list_display  = ('provider', 'rate')
        search_fields = ['provider']


class user_agent(models.Model):
    name        = models.CharField(max_length=255, unique=True)
    partner     = models.CharField(max_length=255)

    def __str__(self):
        return str("%s (%s)" % (self.name, self.partner))

    class Admin:
        list_display  = ('name', 'partner')
        search_fields = ['name']


