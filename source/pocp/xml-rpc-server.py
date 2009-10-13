# #!/usr/bin/python2.5
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
# The SSL XMP-RPC part ist based on:
# SecureXMLRPCServer.py - simple XML RPC server supporting SSL.
# Based on this article: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/81549

USE_SSL = True

# I did not get a specification for the XML-RPC, so the values are "guessed"

# Configure below
from settings_xml_rpc import LISTEN_IP, LISTEN_PORT, LEASE_FILE, SSL_PEM, SSL_KEY, API_VERSION
if not LISTEN_IP:
  LISTEN_IP = "127.0.0.1"

import SocketServer
import BaseHTTPServer
import SimpleHTTPServer
import SimpleXMLRPCServer

import socket, os
from OpenSSL import SSL

class SecureXMLRPCServer(BaseHTTPServer.HTTPServer,SimpleXMLRPCServer.SimpleXMLRPCDispatcher):
    def __init__(self, server_address, HandlerClass, logRequests=True):
        """Secure XML-RPC server.

        It it very similar to SimpleXMLRPCServer but it uses HTTPS for transporting XML data.
        """
        self.logRequests = logRequests

        try:
	    SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self)
        except TypeError:
            # An exception is raised in Python 2.5 as the prototype of the __init__
            # method has changed and now has 3 arguments (self, allow_none, encoding)
            SimpleXMLRPCServer.SimpleXMLRPCDispatcher.__init__(self, False, None)
        SocketServer.BaseServer.__init__(self, server_address, HandlerClass)
        ctx = SSL.Context(SSL.SSLv23_METHOD)
        ctx.use_privatekey_file (SSL_KEY)
        ctx.use_certificate_file(SSL_PEM)
        self.socket = SSL.Connection(ctx, socket.socket(self.address_family,
                                                        self.socket_type))
        self.server_bind()
        self.server_activate()

class SecureXMLRpcRequestHandler(SimpleXMLRPCServer.SimpleXMLRPCRequestHandler):
    """Secure XML-RPC request handler class.

    It it very similar to SimpleXMLRPCRequestHandler but it uses HTTPS for transporting XML data.
    """
    def setup(self):
        self.connection = self.request
        self.rfile = socket._fileobject(self.request, "rb", self.rbufsize)
        self.wfile = socket._fileobject(self.request, "wb", self.wbufsize)
        
    def do_POST(self):
        """Handles the HTTPS POST request.

        It was copied out from SimpleXMLRPCServer.py and modified to shutdown the socket cleanly.
        """

        try:
            # get arguments
            data = self.rfile.read(int(self.headers["content-length"]))
            # In previous versions of SimpleXMLRPCServer, _dispatch
            # could be overridden in this class, instead of in
            # SimpleXMLRPCDispatcher. To maintain backwards compatibility,
            # check to see if a subclass implements _dispatch and dispatch
            # using that method if present.
            response = self.server._marshaled_dispatch(
                    data, getattr(self, '_dispatch', None)
                )
        except: # This should only happen if the module is buggy
            # internal error, report as HTTP server error
            self.send_response(500)
            self.end_headers()
        else:
            # got a valid XML RPC response
            self.send_response(200)
            self.send_header("Content-type", "text/xml")
            self.send_header("Content-length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)

            # shut down the connection
            self.wfile.flush()
            self.connection.shutdown() # Modified here!
    
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

########################################
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
        
def test(HandlerClass = SecureXMLRpcRequestHandler,ServerClass = SecureXMLRPCServer):
    """Test xml rpc over https server"""
    class xmlrpc_registers:
        def __init__(self):
            import string
            self.python_string = string
            
        def test_add(self, x, y):
            return x + y
    
        ########################################
        def is_auth(self, myhandle):
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
        # /xmlrpc/presence.php
        def getClientStatus(self, ip):
          """
          Returns the status information of a client.
          @parameters:
            ip: string, The IPv4 address of the client.
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
          from helper.dhcpd import parse_lease_file
          for row in parse_lease_file(LEASE_FILE):
            if row['ip'] == ip:
              return { 'alive': True, 'mac': row['mac'] }
          return { 'status': False, 'mac': '' }
        
        ########################################
        # /xmlrpc/sessionmanager.php
        def getActiveSessions(self, handle):
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
        
          from helper.dhcpd import parse_lease_file
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
              a['end']   = leases[ip]['end']
              a['start'] = leases[ip]['start']
              a['mac']   = leases[ip]['mac']
              # Only return active_route as active, if there is a dhcp lease (?)
              ret.append(a)
          return ret
        
        def stopSession(self, handle, address):
          """
          Stopps an active sessions.
          @parameters:
            handle:  string, The Authentication Handle (see /xmlrpc/authenticator.php -> login)
            address: string, IPv4 address of the Session to stop.
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
        
          return True
        
        ########################################
        # /xmlrpc/authenticator.php
        def login(self, username, password):
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
        
        def logout(self, myhandle):
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
        
        def getApiVersion(self):
          """
          Returns the API version number of the XMLRPC-API.
          @returns:
            int
          """
          return API_VERSION
        
    server_address = (LISTEN_IP, LISTEN_PORT) # (address, port)
    server = ServerClass(server_address, HandlerClass)    
    server.register_instance(xmlrpc_registers())    
    sa = server.socket.getsockname()
    print "Serving HTTPS on", sa[0], "port", sa[1]
    server.serve_forever()

if __name__ == '__main__':
    test()


