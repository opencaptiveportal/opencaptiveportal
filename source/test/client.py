#!/usr/bin/python

# To test the XML-RPC server

import xmlrpclib

print "DEBUG: Start"
proxy = xmlrpclib.ServerProxy("https://127.0.0.1:1443/xmlrpc/presence.php")
print "DEBUG: Connected to XML-RPC"

#print "Ausgabe vom XML-RPC:", str(proxy.presence())
#print proxy.system.listMethods()
#print proxy.system.methodHelp("presence")
print "DEBUG: getApiVersion:", proxy.getApiVersion()

print "DEBUG: Login"
user   = raw_input("User: ")
passwd = raw_input("Password: ")
handle = str(proxy.login( user, passwd ) )
print "DEBUG: Got handle:", handle

print "DEBUG: getActiveSessions:", str(proxy.getActiveSessions(handle))
print "DEBUG: getClientStatus:",   str(proxy.getClientStatus('10.1.2.23'))

#print "DEBUG: stopSession:",       str(proxy.stopSession( handle, '10.136.128.209' ))

print "DEBUG: Logout:", proxy.logout( handle )

