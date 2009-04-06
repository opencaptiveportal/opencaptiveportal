#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

from pocp.helper.iptables import show_iptables, make_iptables
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm

## TODO CHECK, that loggedIn !!!
def show(request, error = None):
  """
  Show the iptables
  """
  out = show_iptables()
  return render_to_response('iptables_show.htm', {
      'iptables': out,
      'error':    error,
    })

def rebuild(request):
  """
  Rebuild the ip[6]tables
  """
  p = make_iptables()
  return render_to_response('iptables_show.htm', {
      'iptables': p.stdout.read(),
      'error':    p.stderr.read(),
    })

