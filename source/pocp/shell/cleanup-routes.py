#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Clean up old sessions

import sys
sys.path.append("../../")

from pocp.settings_xml_rpc import LEASE_FILE
from pocp.helper.dhcpd import parse_lease_file
from pocp.ocp.models import active_route, active_conf

# 1)  active_route, active_conf
#     All entries in active_route and active_conf without (active) DHCP lease
#     (e.g., timeout)
leases = parse_lease_file(LEASE_FILE, sorted = 'ip')
ret    = [] 

route_conf_list = list( active_route.objects.all() )
route_conf_list.extend( list( active_conf.objects.all() ) ) 
for row in route_conf_list:
  # Check, that there is a valid lease file without timeout
  ip = row.src_ip
  if leases.has_key(ip):
    if leases[ip]['bstate'] == 'active':
      continue
  # Delete entry
  try:
    row.delete()
  except:
    print "ERROR: Could not delete route for object", row

