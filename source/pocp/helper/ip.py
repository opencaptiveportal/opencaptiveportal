#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Helper functions for GRE tunnels and ip rules


class iptExc(Exception):
  """
  Custom exception
  """
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)


def delete_tunnel(gre_tunnel):
  """
  Delete a GRE tunnel.
  """
  import os
  # routing tables are delete with the GRE tunnels
  # rules have to be deleted separately
  try:
    os.system("""
        /usr/bin/sudo /bin/ip tunnel del gre%i >/dev/null 2>&1
        /usr/bin/sudo /bin/ip rule del fwmark %s lookup %s >/dev/null 2>&1
      """ % (gre_tunnel, str(hex(gre_tunnel)), str(gre_tunnel)))
  except:
    raise iptExc("Could not delete GRE tunnel gre%i" % (gre_tunnel, ))
  return True


def create_tunnel(gre_tunnel, local_ipv4, remote_ipv4, int_ipv4):
  """
  Create a GRE tunnel.
  """
  import os
  def raise_gre():
    raise iptExc("Could not create GRE tunnel gre%i with local IPv4 %s and remote IPv4 %s" % (gre_tunnel, local_ipv4, remote_ipv4))
  def raise_ip():
    raise iptExc("Could not add IP addresse %s to GRE tunnel gre%i" % (int_ipv4, gre_tunnel))
  # Setting ip rule
  try:
    ret = os.system("""
        /usr/bin/sudo /bin/ip rule add fwmark %s lookup %s
      """ % (str(hex(gre_tunnel)), str(gre_tunnel)) )
  except:
    raise iptExc("Could not set ip ru for gre tunnel %s" % str(gre_tunnel) )
  # Setting GRE tunnel
  try:
    ret = os.system("""
        /usr/bin/sudo /bin/ip tunnel add gre%i mode gre remote %s local %s;
        /usr/bin/sudo /bin/ip link set dev gre%i up
      """ % (gre_tunnel, remote_ipv4, local_ipv4, gre_tunnel))
    if ret != 0:
      raise_gre()
  except:
    raise_gre()
  # Setting IP configuration
  try:
    ret = os.system("""
        /usr/bin/sudo /bin/ip addr  add %s/30 dev gre%i
        /usr/bin/sudo /bin/ip route add default dev gre%i table %i
      """ % (int_ipv4, gre_tunnel, gre_tunnel, gre_tunnel))
    if ret != 0:
      raise_ip()
  except:
    raise_ip()
  return True


def create_all_gre():
  """
  Create all GRE tunnels and IP configurations
  """
  from pocp.ocp.models import provider
  import os
  ret = True
  for p in provider.objects.all():
    try:
      delete_tunnel(p.gre_tunnel)
    except:
      pass
    create_tunnel(p.gre_tunnel, p.local_ipv4, p.remote_ipv4, p.int_ipv4)
  return True


def delete_all_gre():
  """
  Delete all GRE tunnels and IP configurations
  """
  from pocp.ocp.models import provider
  import os
  ret = True
  for p in provider.objects.all():
    try:
      delete_tunnel(p.gre_tunnel)
    except:
      pass
  return True

