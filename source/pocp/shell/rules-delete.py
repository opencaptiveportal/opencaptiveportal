#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Start the iptables

import sys
sys.path.append("../../")

# Delete rules and GRE tunnels
from pocp.helper.ip import delete_all_gre
p = delete_all_gre()


