#!/usr/bin/python
#  -*- coding: UTF-8 -*-
# vim: set fileencoding=UTF-8 :

# Start the iptables

import sys
sys.path.append("../../")
from pocp.helper.iptables import make_iptables

p = make_iptables()

