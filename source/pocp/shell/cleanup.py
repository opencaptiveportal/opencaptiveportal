#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Clean up old sessions
# All entries in active_route and active_conf without DHCP lease or timeouted

import sys
sys.path.append("../../")

from pocp.settings_xml_rpc import LEASE_FILE
from pocp.helper.dhcpd import parse_lease_file
from pocp.ocp.models import active_route, active_conf

leases = parse_lease_file(LEASE_FILE, sorted = 'ip')
ret    = [] 

for row in active_route.objects.all(),
        active_conf.objects.all():
  # Check, that there is a valid lease file without timeout
  if leases.has_key(ip):
    continue
  # Delete entry
  try:
    row.delete()
  except:
    print "ERROR: Could not delete route for object", row

  
  ip       = str(row.src_ip)
  provider = str(row.provider.name)
  a = { 
      'profile':  provider,
      'end':      '',  # None
      'presence': '',  # None
      'address':  ip,
      'start':    '',  # None
      'mac':      '',  # None
      'provider': provider,
      'glue':     '',  # ??
      'type':     '',  # ??
      'id':       '',  # None
    } 
  if leases.has_key(ip):
    a['end']   = leases['ip']['end']
    a['start'] = leases['ip']['start']
    a['mac']   = leases['ip']['mac']
    # Only return active_route as active, if there is a dhcp lease (?)
    ret.append(a)
return ret


