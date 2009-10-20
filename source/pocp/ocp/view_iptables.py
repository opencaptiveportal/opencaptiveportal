#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

from pocp.helper.iptables import show_iptables, make_iptables
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# For all views, check that there is an authentication
@login_required
def show(request, error = None):
  """
  Show the iptables
  """
  if not request.user.is_staff:
    return render_to_response('error.htm', {
        'error': "Sorry, you are not staff... (user permissions 'is_staff')",
      })
  out = show_iptables()
  return render_to_response('iptables_show.htm', {
      'iptables': out,
      'error':    error,
    })

@login_required
def rebuild(request):
  """
  Rebuild the ip[6]tables
  """
  if not request.user.is_staff:
    return render_to_response('error.htm', {
        'error': "Sorry, you are not staff... (user permissions 'is_staff')",
      })
  p = make_iptables()
  return render_to_response('iptables_show.htm', {
      'iptables': p.stdout.read(),
      'error':    p.stderr.read(),
    })

