#!/usr/bin/python2.4
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :
# 
# +------------------------------------------------+
# | OpenCaptivePortal                              |
# |                                                |
# | For further information please see             |
# |    http://code.google.com/p/opencaptiveportal/ |
# | or                                             |
# |    http://www.switch.ch/mobile/pwlan/          |
# +------------------------------------------------+
# 

# I did not get a specification for the XML-RPC, so the values are "guessed"

# Config
import socket
from settings_xml_rpc import LISTEN_IP, LISTEN_PORT, LEASE_FILE, SSL_PEM, API_VERSION
from helper.dhcpd import parse_lease_file
from SecureXMLRPCServer import SecureXMLRPCServer, SecureXMLRPCRequestHandler

if not LISTEN_IP:
  LISTEN_IP = socket.gethostbyname(socket.getfqdn())

class RequestHandler(SecureXMLRPCRequestHandler):
  rpc_paths = ('/RPC2','/xmlrpc/presence.php',)

server = SecureXMLRPCServer((LISTEN_IP, LISTEN_PORT), SSL_PEM, SSL_PEM, handler = RequestHandler)

print "DEBUG: Listening on", LISTEN_IP, "port", LISTEN_PORT, "..."
  
server.register_introspection_functions()


########################################
# /xmlrpc/presence.php
def getClientStatus(ip):
  """
  Returns the status information of a client.
  @parameters:
    ip: string, The IP Address of the client.
  @returns:
    If Client is alive:
      dict: { 'alive':  Bool,   True,
              'mac':    string, <MAC address of client>,
            }
    If Client is not alive/present:
      dict: { 'status': Bool,   False,
              'mac':    string, ''
            }
  """
  if ip is None:
    return { 'status': False, 'mac': '' }
  for row in parse_lease_file(LEASE_FILE):
    if row['ip'] == ip:
      return { 'alive': True, 'mac': row['mac'] }
  return { 'status': False, 'mac': '' }
server.register_function(getClientStatus)

########################################
# /xmlrpc/sessionmanager.php
def getActiveSessions(handle):
  """
  Returns a list of active sessions.
  @parameters:
    handle: string, The Authentication Handle (see /xmlrpc/authenticator.php -> login)
  @returns:
    array of hashs:
    [ { 'profile':  'switch',      -- ('switch', 'swisscom', ... )
        'end':      '1232726400',  -- unix timestamp
        'presence': 'arp://arp',   -- ??
        'address':  'a.b.c.d',     -- IPv4 address 
        'start':    '1232699825',  -- unix timestamp
        'mac':      'a:b:c:d:e:f', -- MAC address
        'provider': 'switch',      -- ('switch', 'swisscom', ... )
        'glue':     '',            -- ??
        'type':     'login',       -- ('login', 'route', ... )
        'id':       '1086',        -- integer
      }, ... ] 
  """
  is_auth(handle)

  leases = parse_lease_file(LEASE_FILE, sorted = 'ip')
  ret = []

  from ocp.models import active_route

  for row in active_route.objects.all():
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
server.register_function(getActiveSessions)

def stopSession(handle, address):
  """
  Stopps an active sessions.
  @parameters:
    handle:  string, The Authentication Handle (see /xmlrpc/authenticator.php -> login)
    address: string, Address of the Session to stop.
  @returns:
    Bool
  """
  is_auth(handle)
  from helper.iptables import delete_route
  from ocp.models import active_route

  # delete route in database
  delete_route(address)
  # delete route in iptables
  try:
    active_route.objects.get(src_ip = address).delete()
  except active_route.DoesNotExist:
    pass

  return ret
server.register_function(stopSession)

########################################
# Exception
class Fault(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

########################################
def delete_old_handles():
  """
  Helperfunction.
  """
  from xml_rpc.models import handle
  from settings_xml_rpc import HANDLE_TIMEOUT
  from datetime import timedelta, datetime
  timeout = datetime.now() - timedelta(seconds = HANDLE_TIMEOUT)
  # TODO: This here does not perfom, please do it (in the future?) direct with sql.
  for h in handle.objects.all():
    if timeout > h.last_seen:
      h.delete() 
  return True

def is_auth(myhandle):
  """
  Helperfunction.
  """
  delete_old_handles()

  import time
  from xml_rpc.models import handle
  try:
    h = handle.objects.get(handle = myhandle)
  except:
    raise Fault, 'handle is invalid'
    #return False

  h.last_seen = time.time()
  return True

########################################
# /xmlrpc/authenticator.php
def login(username, password):
  """
  Checks user credentials and return and handle on success.
  @parameters:
    username: string
    password: string
  @returns:
    string, The Authentication Handle.
            Empty, if Authentication did not work.
  """
  # Until python2.4 use sha, then hashlib
  import sha, random
  from xml_rpc.models import handle
  from django.contrib.auth import authenticate
  user = authenticate(username = username, password = password)
  if user is not None:
    if user.is_active and user.has_perm('xml_rpc.xml_rpc'):
      myhandle = sha.new(str(random.random())).hexdigest()
      try:
        handle.objects.create(user = user, handle = myhandle)
        return myhandle
      except:
        return ''  # ^= False
  return ''  # ^= False
server.register_function(login)

def logout(myhandle):
  """
  Destroy handle.
  @parameters:
    handle: string, The Authentication Handle.
  @returns:
    Bool
  """
  from xml_rpc.models import handle
  try:
    handle.objects.get(handle = myhandle).delete()
  except:
    pass
  return True
server.register_function(logout)

def getApiVersion():
  """
  Returns the API version number of the XMLRPC-API.
  @returns:
    int
  """
  return API_VERSION
server.register_function(getApiVersion)

########################################
#server.serve_forever()
try:
  server.serve_forever()
#  while 1:
#    server.handle_request()
except KeyboardInterrupt:
  server.server_close()

