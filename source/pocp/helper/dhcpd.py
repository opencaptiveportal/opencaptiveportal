#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Helper functions for parsing the dhcpd log

def parse_lease_file(lease_file, sorted = None):
  """
  Parse the DHCP lease file and returns active hosts
  @returns:
    list of dicts with
      {'ip':    <ip>,
       'mac':   <<mac>,
       'start': <start>,
       'end':   <end>,
      }
  """
  import re, sys
  
  # lease 10.4.154.93 {
  #   starts 4 2008/12/04 10:07:00;
  #   ends 4 2008/12/04 22:07:00;
  #   tstp 4 2008/12/04 22:07:00;
  #   binding state free;
  #   hardware ethernet 00:0d:60:2f:2e:fd;
  #   uid "\001\000\015`/.\375";
  # }
  
  # important:
  #   strip newline
  #   delimiter := "}"
  lease = re.compile(r""".*
  lease\ (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*
  starts\ \d\ (?P<starts>\d{4}/\d{2}/\d{2}\ \d{2}:\d{2}:\d{2}).*
  ends\ \d\ (?P<ends>\d{4}/\d{2}/\d{2}\ \d{2}:\d{2}:\d{2}).*
  hardware\ ethernet\ (?P<mac>([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}).*
  .*""", re.VERBOSE)
  
  fd = open(lease_file, "r")
  text = fd.read()
  fd.close()
  
  text = text.replace('\n','')
  textl = text.split('}')
  
  if sorted == 'ip':
    ll = {}
    for i in textl:
      if lease.match(i):
        ip = lease.match(i).group('ip')
        if not ll.has_key(ip):
          ll[ip] = {'mac':   lease.match(i).group('mac'),
                    'start': lease.match(i).group('starts'),
                    'end':   lease.match(i).group('ends'),
                   }
    return ll
  else:
    ll = []
    for i in textl:
      if lease.match(i):
        m = {'ip':    lease.match(i).group('ip'),
             'mac':   lease.match(i).group('mac'),
             'start': lease.match(i).group('starts'),
             'end':   lease.match(i).group('ends'),
            }
        ll.append(m) 
    return ll

