#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Helper functions for active directory auth

# Copied from http://www.djangosnippets.org/snippets/901/
# and modified 

import settings
import ldap 
import sys

try:
  DEBUG = settings.AD_DEBUG
except:
  DEBUG = 1

class ActiveDirectoryGroupMembershipSSLBackend:
  def authenticate( self, username = None, password = None ):
    if len( password ) == 0:
      return None
    return self.get_or_create_user( username, password )

  # If a user does not exist in django, we will try to fetch the user from ldap
  # and create a django account
  def get_or_create_user(self, username, password):
    if DEBUG:
      sys.stderr.write("ldap-auth:  User", username, "*************\n")
      sys.stderr.flush()
    from django.contrib.auth.models import User, Group
    try:
      user = User.objects.get( username = username )
      return user
    except User.DoesNotExist:
      pass
    # User does not exist,
    # => 1.  try to fetch the user from ldap
    #    2.  create django user account with group "ldap"
    if DEBUG:
      sys.stderr.write("ldap-auth:  User", username, "does not exist in django.\n")
      sys.stderr.flush()
    # Connection to ldap
    try:
      ldap.set_option( ldap.OPT_X_TLS_CACERTFILE, settings.AD_CERT_FILE )
      ldap.set_option( ldap.OPT_REFERRALS, 0 ) # DO NOT TURN THIS OFF OR SEARCH WON'T WORK!      
      # Initialize
      if DEBUG:
        sys.stderr.write("ldap-auth:  ldap.initialize...\n")
        sys.stderr.flush()
      l = ldap.initialize( settings.AD_LDAP_URL )
      l.set_option( ldap.OPT_PROTOCOL_VERSION, 3 )
      if DEBUG:
        sys.stderr.write("ldap-auth:  ldap.bind...\n")
        sys.stderr.flush()
      binddn = "%s@%s" % ( username, settings.AD_NT4_DOMAIN )
      l.bind_s( binddn, password )
    except:
      sys.stderr.write("ldap-auth:  ldap connection did not work!\n")
      sys.stderr.flush()
      return None

    if DEBUG:
      sys.stderr.write("ldap-auth:  search...\n")
      sys.stderr.flush()
    result = l.search_ext_s( settings.AD_SEARCH_DN, ldap.SCOPE_SUBTREE, "sAMAccountName=%s" % username, settings.AD_SEARCH_FIELDS )[0][1]
    if DEBUG: 
      sys.stderr.write("ldap-auth:  result:", result)
      sys.stderr.flush()
    # Validate that they are a member of review board group
    if result.has_key('memberOf'):
      membership = result['memberOf']
    else:
      membership = None
    if DEBUG:
      sys.stderr.write("ldap-auth:  required:", settings.AD_MEMBERSHIP_REQ)
      sys.stderr.flush()
    bValid=0
    for req_group in settings.AD_MEMBERSHIP_REQ:
      if DEBUG:
        sys.stderr.write("ldap-auth:  Check for %s group..." % req_group)
        sys.stderr.flush()
      for group in membership:
        group_str = "CN=%s," % req_group
        if group.find( group_str ) >= 0:
          if DEBUG:
            sys.stderr.write("ldap-auth:  User authorized: group_str membership found!\n")
            sys.stderr.flush()
          bValid=1
          break
    # No result => exit
    if bValid == 0:
      if DEBUG:
        sys.stderr.write("ldap-auth:  User not authorized, correct group membership not found!\n")
        sys.stderr.flush()
      return None
    # Get additional information to the found result
    # get email
    mail = None
    if result.has_key('mail'):
      mail = result['mail'][0]
    if DEBUG:
      sys.stderr.write("ldap-auth:  email:", mail)
      sys.stderr.flush()
    # get surname
    last_name = None
    if result.has_key('sn'):
      last_name = result['sn'][0]
    if DEBUG:
      sys.stderr.write("ldap-auth:  sn=%s" % last_name)
      sys.stderr.flush()
    # get display name
    first_name = None
    if result.has_key('givenName'):
      first_name = result['givenName'][0]
    if DEBUG:
      sys.stderr.write("ldap-auth:  first_name=%s" % first_name)
      sys.stderr.flush()
    l.unbind_s()
    # Create and save user
    user = User(username=username,first_name=first_name,last_name=last_name,email=mail)
    user.is_staff     = False
    user.is_superuser = False
    import random
    user.set_password( str( random.random() ) )
    user.save()
    # add user to "ldap" group
    try:
      group = Group.objects.get(name = "ldap")
    except:
      group = Group(name = "ldap")
      group.save()
    if DEBUG:
      sys.stderr.write("ldap-auth:  group:", group)
      sys.stderr.flush()
    user.groups.add(group)
    user.save()
    if DEBUG:
      sys.stderr.write("ldap-auth:  end.\n")
      sys.stderr.flush()
    return user

  def get_user(self, user_id):
    from django.contrib.auth.models import User
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None


