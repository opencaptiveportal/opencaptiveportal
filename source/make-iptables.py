#!/usr/bin/python2.4
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 tabstop=4 shiftwidth=4 expandtab :
# 
# +------------------------------------------------+
# | OpenCaptivePortal                              |
# |                                                |
# | For further information please see             |
# |    http://code.google.com/p/opencaptiveportal/ |
# | or                                             |
# |    http://www.switch.ch/mobile/pwlan/          |
# +------------------------------------------------+
# 

# This scripts downloads the SWITCHclassic ACls 
# and creates with the template file "iptables.tmpl" 
# the iptables-restore file for the OpenCaptivePortal

# Config
# SWITCHclassic ACLs
acl_url = "https://www.switch.ch/cgi-bin/mobile/acl"

def usage():
  print "usage: %s  db_file tmpl_file  output_file" % sys.argv[0]
  print "       %s  /var/lib/opencaptiveportal/pwlan.db /etc/opencaptiveportal/iptables.tmpl /tmp/iptables-restore" % sys.argv[0]
  sys.exit(9)

import sys
if len(sys.argv) == 4:
  # SQLite3 DB
  sqlite3_db  = sys.argv[1]
  tmpl_file   = sys.argv[2]
  output_file = sys.argv[3]
else:
  usage()

from Cheetah.Template import Template
import urllib2
from pysqlite2 import dbapi2 as sqlite3


try:
  con = sqlite3.connect(sqlite3_db)
except:
  print "%s: Cannot open SQLite DB file %s" % (sys.argv[0], sqlite3_db)
  sys.exit(9)
cur = con.cursor()

# wisps = ({'id': 1, 'hexid': '01'},
#          {'id': 2, 'hexid': '02'},
#          {'id': 3, 'hexid': '03'},
#          {'id': 5, 'hexid': '04'},
# 	)
cur.execute("""SELECT gre_tunnel FROM provider;""")
wisps = []
for row in cur.fetchall():
  wisps.append({'id': row[0], 'hexid': hex(row[0])})
# active_session = (('192.168.1.1',  '01'),
#                   ('192.168.2.34', '02'),
# 		 )
cur.execute("""SELECT src_ip, provider_id FROM active_routes;""")
active_session = []
for row in cur.fetchall():
  active_session.append((row[0], row[1]))

# SWITCHclassis ACLs holen
opener = urllib2.build_opener()
acls_raw = opener.open(acl_url)
acls_raw = acls_raw.readlines()
classic_acls = []
for line in acls_raw:
  line = line.strip()
  classic_acls.append(line.split(" "))

fp = open(tmpl_file, 'r')
tmpl = fp.read()
fp.close()

fp = open(output_file, 'w')
fp.write(str(Template(tmpl, 
        searchList=[{'wisps':           wisps,
                     'active_session':  active_session,
                     'classic_acls':    classic_acls,
                    }])))
fp.close()

