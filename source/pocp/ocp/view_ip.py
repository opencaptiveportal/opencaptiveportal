#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

from pocp.helper.ip import make_gre_tunnel
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm

## TODO CHECK, that loggedIn !!!
def show(request):
  """
  View the IP configuration
  """
  import subprocess
  p = subprocess.Popen(["""echo "ip addr list"; /bin/ip addr list; echo; echo; echo "ip route list"; /bin/ip route list;"""],
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return render_to_response('ip_show.htm', {
      'ip':     p.stdout.read(),
      'error':  p.stderr.read(),
    })

def rebuild(request):
  """
  Rebuild the IP configuration
  """
  make_gre_tunnel()
  return show(request)

