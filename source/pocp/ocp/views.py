#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import AuthenticationForm

## IMPORTANT TODO
## The admin stuff is very alpha, e.g. there is no real auth, CHECK THAT bevor commit !!1!
def admin(request):
  """
  Overview for the Administrators
  """
  loggedin = False
  if str(request.user) != "AnonymousUser":
    loggedin = True
  return render_to_response('admin.htm', {
      'username': request.user,
      'loggedin': loggedin,
    })

def add_active_route(src_ip, prov = None, conf = None):
  from pocp.ocp.models import provider, active_route, active_conf
  from settings import GRE_TUNNEL_CONF
  if not conf and prov is None:
    return False
  if conf:
    try:
      a = active_conf.objects.get(src_ip = src_ip)
      a.delete()
    except:
      pass
    a = active_conf(src_ip = src_ip)
    return a.save()
  # not conference
  elif type(prov) in (unicode, str):
    prov = provider.objects.get(name = prov)
  # Delete existing active_route to src_ip, just to be sure
  try:
    a = active_route.objects.get(src_ip = src_ip)
    a.delete()
  except:
    pass
  # And save new route 
  a = active_route(src_ip = src_ip, provider = prov)
  return a.save()

def landingpage(request):
  """
  Show the Landingpage"
  """
  from pocp.ocp.models import provider, round_robin
  from random import random
  # User-Agent: iPassConnect (iPass)
  if request.META.has_key('HTTP_USER_AGENT'):
    if request.META['HTTP_USER_AGENT'] == 'iPassConnect':
      src_ip  = request.META['REMOTE_ADDR']
      # Round Robin for WISP
      my_random = random()
      for obj in round_robin.objects.all():
        if my_random <= obj.rate:
          prov = obj
          break
        else:
          my_random -= obj.rate
      # Add and save new route
      add_active_route(src_ip = src_ip, prov = prov)
      return render_to_response('ipass.htm', {})
  # /User-Agent

  # See django.contrib.auth.views, login:
  redirect_to = '/'
  loggedin = False
  if str(request.user) != "AnonymousUser":
    loggedin = True
  if request.method == "POST":
    form = AuthenticationForm(data=request.POST)
    if str(request.user) != "AnonymousUser":
      from django.contrib.auth.views import logout
      logout(request, '/')
      return HttpResponseRedirect('/')
    if form.is_valid():
      # Light security check -- make sure redirect_to isn't garbage.
      if not redirect_to or '//' in redirect_to or ' ' in redirect_to:
        redirect_to = settings.LOGIN_REDIRECT_URL
      from django.contrib.auth import login
      login(request, form.get_user())
      # If the user wants internet (he is coming from the landingepage and not
      # i.e. admin login)
      give_internet = request.POST.get('give_internet','0')
      if give_internet:
        try:
          src_ip = request.META['REMOTE_ADDR']
          try:
            add_active_route(src_ip = src_ip, prov = None, conf = True)
            print "DEBUG: Activated conf for src_ip", src_ip
          except:
            print "ERROR: Could not activate route for src_ip", src_ip, "(conference modus)."
        except:
          pass
      if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
      return HttpResponseRedirect(redirect_to)
  else:
    form = AuthenticationForm(request)
  request.session.set_test_cookie()
  url = None
  if request.GET.has_key('url'):
    url = request.GET['url']
  else:
    url = request.build_absolute_uri()

  # Round Robin for WISP
  provs = []
  for prov in round_robin.objects.all():
    if prov.provider.iframe_url != '':
      provs.append(prov)
  sorted_provs = []
  last = 0
  while len(provs) > 0:
    my_random = random() - last
    for prov in provs:
      if my_random <= prov.rate:
        prov.provider.iframe_url = prov.provider.iframe_url.replace("{{ site }}", request.META['SERVER_NAME'])
        prov.provider.iframe_url = prov.provider.iframe_url.replace("{{ url }}", url)
        sorted_provs.append(prov.provider)
        last += prov.rate
        provs.remove(prov)
        break
      else:
        my_random -= prov.rate

  # than, repace the rest of the template
  return render_to_response('landingpage.htm', {
      'username': request.user,
      'loggedin': loggedin,
      'form':     form,
      'wisps':    sorted_provs,
    })


def route(self):
  """
  Add a route for src_ip to Provider with provider
  """
  # TODO: wenn keine url, herausfinden, welche ????
  # TODO: wenn url = hostname (fqdn), dann -> google.ch
  if not (self.META.has_key('REMOTE_ADDR') and 
          self.GET.has_key('provider')):
          #self.GET.has_key('url')):
    #return HttpResponseRedirect('/index.php')
    # TODO: Auf die Fehlerseite Link zu back.php
    return render_to_response('error.htm', {
        'error': "Falsche Parameter auf route.php",
      })
  src_ip = self.META['REMOTE_ADDR']
  prov   = self.GET['provider']
  url    = "http://www.google.ch"
  if self.GET.has_key('url'):
    url   = self.GET['url']
  # Add and save new route
  add_active_route(src_ip = src_ip, prov = prov)
  return HttpResponseRedirect(url)


def back(self):
  """
  Delete _ALL_ routes for src_ip
  """
  from pocp.ocp.models import active_route

  if not (self.META.has_key('REMOTE_ADDR')):
    return render_to_response('error.htm', {
        'error': "Falsche Parameter auf back.php",
      })
  src_ip = self.META['REMOTE_ADDR']

  # Delete entry in DB
  try:
    a = active_route.objects.get(src_ip = src_ip)
    a.delete()
  except active_route.DoesNotExist:
    pass

  return HttpResponseRedirect('/index.php')

