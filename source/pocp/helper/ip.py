#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Helper functions for GRE tunnels


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
  try:
    os.system("""
        /usr/bin/sudo /bin/ip tunnel del gre%i
      """ % (gre_tunnel, ))
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
  try:
    ret = os.system("""
        /usr/bin/sudo /bin/ip tunnel add gre%i mode gre remote %s local %s;
        /usr/bin/sudo /bin/ip link set dev gre%i up
      """ % (gre_tunnel, remote_ipv4, local_ipv4, gre_tunnel))
    if ret != 0:
      raise_gre()
  except:
    raise_gre()
  try:
    ret = os.system("""
        /usr/bin/sudo /bin/ip addr add %s/30 dev gre%i
      """ % (int_ipv4, gre_tunnel))
    if ret != 0:
      raise_ip()
  except:
    raise_ip()
  return True


def make_gre_tunnel():
  """
  Renew all GRE Tunnel and IP addresses. 
  """
  from pocp.ocp.models import provider
  import os
  ret = True
  for p in provider.objects.all():
    delete_tunnel(p.gre_tunnel)
    create_tunnel(p.gre_tunnel, p.local_ipv4, p.remote_ipv4, p.int_ipv4)
  return True


