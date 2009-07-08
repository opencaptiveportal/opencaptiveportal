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
        /usr/bin/sudo /sbin/iptables -t mangle -A PREROUTING -s %s -j MARK --set-mark %s
      """ % (src_ip, gre_tunnel))
  except:
    raise iptExc("Could not insert route from src_ip %s to gre tunnel %s in iptables" % (src_ip, gre_tunnel))
  return True


def insert_conf(src_ip):
  """
  Inserta a route with source ip sc_ip, member of a conference
  """
  from settings import GRE_TUNNEL_CONF
  return insert_route(src_ip, GRE_TUNNEL_CONF)


def delete_route(src_ip):
  """
  Delete the route with source ip src_ip.
  """
  import os
  # no while loop (is better...)
  try:
    print os.system("""
        count=`/usr/bin/sudo /sbin/iptables -t mangle -nv --list PREROUTING | grep " %s " | wc -l`
        for i in `seq 1 $count`; do
          a=`/usr/bin/sudo /sbin/iptables --line-numbers -t mangle -nv --list PREROUTING | grep " %s " | cut -d" " -f 1 | head -n 1`;
          [ "$a" ] && /usr/bin/sudo /sbin/iptables -t mangle -D PREROUTING $a;
        done
      """ % (src_ip, src_ip))
  except:
    raise iptExc("Could not delete route from src_ip %s in iptables" % (src_ip))
  return True
    

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
    active_sessions.append( ( p.src_ip, p.provider.gre_tunnel ) )

  # replace variables in template file
  iptables_restore = render_to_string(IPTABLES_TMP_FILE, 
          { 'wisps':           wisps,
            'active_session':  active_sessions,
            'classic_acls':    fetch_switch_classic(),
          } ).encode("utf-8")

  # Debug
  if tmp_file:
    fp = open(tmp_file, 'w')
    fp.write(iptables_restore)
    fp.close()
  import subprocess
  return subprocess.Popen(["""echo "%s" | /usr/bin/sudo /sbin/iptables-restore; echo "%s" """ % (iptables_restore, iptables_restore)],
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def show_iptables():
  """
  Show live iptables
  """
  import subprocess
  out = ""
  out += "\n* iptables -t mangle \n"
  out += subprocess.Popen(["/usr/bin/sudo /sbin/iptables --list -nv -t mangle"], 
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.read()
  out += "\n* iptables -t nat \n"
  out += subprocess.Popen(["/usr/bin/sudo /sbin/iptables --list -nv -t nat"], 
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.read()
  out += "\n* iptables -t filter \n"
  out += subprocess.Popen(["/usr/bin/sudo /sbin/iptables --list -nv -t filter"], 
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.read()
  out += "\n* ip6tables -t mangle \n"
  out += subprocess.Popen(["/usr/bin/sudo /sbin/ip6tables --list -nv -t mangle"], 
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.read()
  out += "\n* ip6tables -t mangle \n"
  out += subprocess.Popen(["/usr/bin/sudo /sbin/ip6tables --list -nv -t filter"], 
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE).stdout.read()
  return out


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
  acls_raw = opener.open(SWITCHclassic_url)
  acls_raw = acls_raw.readlines()
  classic_acls = []
  for line in acls_raw:
    line = line.strip()
    classic_acls.append(line.split(" "))
  return classic_acls

