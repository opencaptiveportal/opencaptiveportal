#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

from pocp.helper.ip import make_gre_tunnel
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# For all views, check that there is an authentication
@login_required
def show(request):
  """
  View the IP configuration
  """
  if not request.user.is_staff:
    return render_to_response('error.htm', {
        'error': "Sorry, you are not staff... (user permissions 'is_staff')",
      })
  import subprocess
  p = subprocess.Popen(["""echo "ip addr list"; /bin/ip addr list; echo; echo; echo "ip route list"; /bin/ip route list;"""],
        shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  return render_to_response('ip_show.htm', {
      'ip':     p.stdout.read(),
      'error':  p.stderr.read(),
    })

@login_required
def rebuild(request):
  """
  Rebuild the IP configuration
  """
  if not request.user.is_staff:
    return render_to_response('error.htm', {
        'error': "Sorry, you are not staff... (user permissions 'is_staff')",
      })
  make_gre_tunnel()
  return show(request)

