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
  LDAP_TMP_GROUP = settings.LDAP_TMP_GROUP
except:
  LDAP_TMP_GROUP = "ldap-tmp-users"

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
      print "ldap-auth:  User", username, "*************"
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
      print "ldap-auth:  User", username, "does not exist in django."
    # Connection to ldap
    try:
      ldap.set_option( ldap.OPT_X_TLS_CACERTFILE, settings.AD_CERT_FILE )
      ldap.set_option( ldap.OPT_REFERRALS, 0 ) # DO NOT TURN THIS OFF OR SEARCH WON'T WORK!      
      # Initialize
      if DEBUG:
        print "ldap-auth:  ldap.initialize..."
      l = ldap.initialize( settings.AD_LDAP_URL )
      l.set_option( ldap.OPT_PROTOCOL_VERSION, 3 )
      if DEBUG:
        print "ldap-auth:  ldap.bind..."
      binddn = "%s@%s" % ( username, settings.AD_NT4_DOMAIN )
      l.bind_s( binddn, password )
    except:
      print "ldap-auth:  ldap connection did not work!"
      return None

    if DEBUG:
      print "ldap-auth:  search..."
    result = l.search_ext_s( settings.AD_SEARCH_DN, ldap.SCOPE_SUBTREE, "sAMAccountName=%s" % username, settings.AD_SEARCH_FIELDS )[0][1]
    if DEBUG: 
      print "ldap-auth:  result:", result
    # Validate that they are a member of review board group
    if result.has_key('memberOf'):
      membership = result['memberOf']
    else:
      membership = None
    if DEBUG:
      print "ldap-auth:  required:", settings.AD_MEMBERSHIP_REQ
    bValid=0
    for req_group in settings.AD_MEMBERSHIP_REQ:
      if DEBUG:
        print "ldap-auth:  Check for %s group..." % req_group
      for group in membership:
        group_str = "CN=%s," % req_group
        if group.find( group_str ) >= 0:
          if DEBUG:
            print "ldap-auth:  User authorized: group_str membership found!"
          bValid=1
          break
    # No result => exit
    if bValid == 0:
      if DEBUG:
        print "ldap-auth:  User not authorized, correct group membership not found!"
      return None
    # Get additional information to the found result
    # get email
    mail = "noreply@localhost.local"
    if result.has_key('mail'):
      mail = result['mail'][0]
    if DEBUG:
      print "ldap-auth:  email:", mail
    # get surname
    last_name = "LDAP"
    if result.has_key('sn'):
      last_name = result['sn'][0]
    if DEBUG:
      print "ldap-auth:  sn=%s" % last_name
    # get display name
    first_name = "LDAP"
    if result.has_key('givenName'):
      first_name = result['givenName'][0]
    if DEBUG:
      print "ldap-auth:  first_name=%s" % first_name
    l.unbind_s()
    # Create and save user
    user = User(username=username, first_name=first_name, last_name=last_name, email=mail)
    user.is_staff     = False
    user.is_superuser = False
    import random
    user.set_password( str( random.random() ) )
    user.save()
    # add user to a temporary group, so that we can delete them later
    try:
      group = Group.objects.get(name = LDAP_TMP_GROUP)
    except:
      group = Group(name = LDAP_TMP_GROUP)
      group.save()
    if DEBUG:
      print "ldap-auth:  group:", group
    user.groups.add(group)
    user.save()
    if DEBUG:
      print "ldap-auth:  end."
    return user

  def get_user(self, user_id):
    from django.contrib.auth.models import User
    try:
      return User.objects.get(pk=user_id)
    except User.DoesNotExist:
      return None


