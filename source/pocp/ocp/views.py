#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Create your views here.

from pocp.helper.iptables import insert_route, delete_route
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

def landingpage(request):
  """
  Show the Landingpage"
  """
  # Von django.contrib.auth.views, login:
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
        # TODO: Mach hier was, damit das geht geht :)
        pass
      if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
      return HttpResponseRedirect(redirect_to)
  else:
    form = AuthenticationForm(request)
  request.session.set_test_cookie()
  return render_to_response('landingpage.htm', {
      'username': request.user,
      'loggedin': loggedin,
      'form':     form,
    })

def route(self):
  """
  Add a route for src_ip to Provider with provider
  """
  if not (self.META.has_key('REMOTE_ADDR') and 
          self.GET.has_key('prov_id') and
          self.GET.has_key('url')):
    return HttpResponseRedirect('/index.php')

  src_ip  = self.META['REMOTE_ADDR']
  prov_id = self.GET['prov_id']
  url     = self.GET['url']

  # If no provider with prov_id exists, an exception will be raised
  prov = provider.objects.get(id = prov_id)

  # Insert route in iptables, if fail -> exception
  insert_route(src_ip, str(prov.gre_tunnel))

  # Delete existing active_route to src_ip, just to be sure
  try:
    a = active_route(src_ip = src_ip)
    a.delete()
  except active_route.DoesNotExist:
    pass

  # And save new route 
  a = active_route(src_ip = src_ip, provider = prov)
  a.save()

  return HttpResponseRedirect(url)


def back(self):
  """
  Delete _ALL_ routes for src_ip
  """
  from pocp.ocp.models import active_route

  if not self.GET.has_key('src_ip'):
    return HttpResponseRedirect('/index.php')
  src_ip = self.GET['src_ip']

  # Delete entry in DB
  try:
    a = active_route.objects.get(src_ip = src_ip)
    a.delete()
  except active_route.DoesNotExist:
    pass
  # and then in iptables
  delete_route(src_ip)

  return HttpResponseRedirect('/index.php')

