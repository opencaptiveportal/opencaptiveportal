#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

##########
# Settings for XML-RPC
#LISTEN_IP   = socket.gethostbyname(socket.getfqdn())
LISTEN_IP   = None # if none, geht from fqdn
LISTEN_PORT = 1443
LEASE_FILE  = "/var/lib/dhcp3/dhcpd.leases"
SSL_PEM     = "/etc/opencaptiveportal/ssl.pem"  # private key and cert
API_VERSION = 0.1

HANDLE_TIMEOUT = 60*5  # 5 minutes
