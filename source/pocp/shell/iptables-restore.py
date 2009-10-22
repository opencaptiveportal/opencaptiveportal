#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Start the iptables

import sys
sys.path.append("../../")

# Reload iptables
from pocp.helper.iptables import make_iptables
p = make_iptables()

# Reload IP configuration and GRE tunnels
from pocp.helper.ip import create_all_gre
p = create_all_gre()

