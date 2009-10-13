#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm

def dhcp(request):
  """
  Text output for provider
  """
  if not request.GET.has_key('ip'):
    return HttpResponse("Not Found\n", mimetype="text/plain")
  else:
    """
    Returns the status information of a client.
    @parameters:
      ip: string, The IPv4 address of the client.
    @returns:
      If Client is alive:
        string:  <client mac address> <client IPv4 address> 0.0.0.0 <starttime> <endtime> <lease time> ISSUED
        <client mac address>:  de:ad:ca:fe:af:fe 
        <client IPv4 address>: a.b.c.d 
        <starttime>:           yyyymmddhhmmss   # in UTC ???
        <stoptime>:            yyyymmddhhmmss   # in UTC ???
        <duration>:            in seconds 
    """
    ip = request.GET['ip']
    if ip is None:
      return HttpResponse("Not Found\n", mimetype="text/plain")
    from helper.dhcpd import parse_lease_file
    try:
      from settings_xml_rpc import LEASE_FILE
    except:
      return HttpResponse("Did not found lease file!\n", mimetype="text/plain")
    for row in parse_lease_file(LEASE_FILE):
      if row['ip'] == ip:
        for i in ( "/", " ", ":" ):
          row['start'] = row['start'].replace( i, "" )
          row['end']   = row['end'].replace(   i, "" )
        return HttpResponse( "%(mac)s %(ip)s 0.0.0.0 %(start)s %(end)s 28800 ISSUED\n" % row, mimetype="text/plain" )
    return HttpResponse("Not Found\n", mimetype="text/plain")



