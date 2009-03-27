#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Helper functions for ipables

# Some constants:
SWITCHclassic_url = "https://www.switch.ch/cgi-bin/mobile/acl"
IPTABLES_TMP_FILE = "iptables-restore.tmpl"


class iptExc(Exception):
  """
  Custom exception
  """
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)


def insert_route(src_ip, gre_tunnel):
  """
  Inserta a route with source ip sc_ip and gre tunnel gre_tunnel
  """
  import os
  try:
    os.system("""
        /usr/bin/sudo /sbin/iptables -t mangle -A PREROUTING -s %s -j MARK --set-mark %i
      """ % (src_ip, gre_tunnel))
  except:
    raise iptExc("Could not insert route from src_ip %s to gre tunnel %i in iptables" % (src_ip, gre_tunnel))

def delete_route(src_ip):
  """
  Delete the route with source ip src_ip.
  """
  import os
  # no while loop (is better...)
  try:
    os.system("""
        count=`/usr/bin/sudo /sbin/iptables -t mangle -nv --list PREROUTING | grep " %s " | wc -l`
        for i in `seq 1 $count`; do
          a=`/usr/bin/sudo /sbin/iptables --line-numbers -t mangle -nv --list PREROUTING | grep " %s " | cut -d" " -f 1 | head -n 1`;
          [ "$a" ] && /usr/bin/sudo /sbin/iptables -t mangle -D PREROUTING $a;
        done
      """ % (src_ip, src_ip))
  except:
    raise iptExc("Could not delete route from src_ip %s in iptables" % (src_ip))
    

def make_iptables(tmp_file = None):
  """
  Build the iptables-restore file and apply it.
  @params:
    tmp_file:   temporary file for iptables-restore data,
                if tmp_file is given, it will not be deleted (for DEBUG purpose)
  Template file for the iptables-restore file:
      pocp/templates/iptables-restore.tmpl
  """
  from django.template.loader import render_to_string
  from pocp.ocp.models import provider, active_route
  import os

  # get provider GRE tunnel ids
  wisps = []
  for p in provider.objects.all():
    wisps.append( { 'id':    p.gre_tunnel,
                    'hexid': hex(p.gre_tunnel) } )

  # get active routes
  active_sessions = []
  for p in active_route.objects.all():
    active_sessions.append( [ p.src_ip, p.provider.gre_tunnel ] )

  # replace variables in template file
  iptables_restore = render_to_string(IPTABLES_TMP_FILE, 
          { 'wisps':           wisps,
            'active_session':  active_sessions,
            'classic_acls':    classic_acls,
          } )

  # Debug
  if tmp_file:
    fp = open(tmp_file, 'w')
    fp.write(iptables_restore)
    fp.close()
  return os.system("""
      echo "%s" | /usr/bin/sudo /sbin/iptables-restore""" % iptables_restore ) 


def make_gre_tunnel(id = None):
  """
  Make the GRE Tunnel with the id.
  If no id is given, make all GRE Tunnels.
  Also set the needed routes and IP adresses for these GRE Tunnel(s).
  Attention: It it delete all existing GRE tunnels with the here given ids.
  """
  from pocp.ocp.models import provider
  import os
  ret = True
  for p in provider.objects.all():
    id = "wisp_%s" % str(p.gre_tunnel)
    # delete gre tunnel:
    #   ip tunnel del gre_100 mode gre 
    if os.system("""/usr/bin/sudo /bin/ip tunnel del %s""" \
        % ( id ) ):
      # create gre tunnel:
      #   ip tunnel add gre_100 mode gre local 130.59.98.210 remote 141.31.176.240
      os.system("""/usr/bin/sudo /bin/ip tunnel add %s mode gre local %s remote %s""" \
          % ( id, p.local_ipv4, p.remote_ipv4 ) )
      # interface ip addresses
      if p.int_ipv4:
        os.system("""/usr/bin/sudo /bin/ip addr add %s dev %s""" % ( p.int_ipv4, id ) )
      if p.int_ipv6:
        os.system("""/usr/bin/sudo /bin/ip addr add %s dev %s""" % ( p.int_ipv6, id ) )
    else:
      ret = False
  return ret


def fetch_switch_classic(url = SWITCHclassic_url):
  """
  Fetch the SWITCHConnect Classic ACLs.
  For more information see: https://www.switch.ch/mobile/classic/
  @params:
    url:   URL to the SWITCHConnect Classic ACLs.
  @return:
    list of lists with IP net and description:
        [ [ <net>, <desc> ], ... ]
    Example:
        [ [ "129.132.99.160/28", "ETHZ" ],
          [ "130.59.108.50/32",  "SWITCH_5" ], 
          [ "130.59.108.51/32",  "SWITCH_6" ], 
          ... ]
  """
  import urllib2
  # SWITCHclassis ACLs holen
  opener = urllib2.build_opener()
  acls_raw = opener.open(acl_url)
  acls_raw = acls_raw.readlines()
  classic_acls = []
  for line in acls_raw:
    line = line.strip()
    classic_acls.append(line.split(" "))
  return classic_acls

