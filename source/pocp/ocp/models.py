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


class provider(models.Model):
    name        = models.CharField(max_length=255, unique=True)
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

