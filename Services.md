This page gives an overview of the services and daemons, which have to run on the opencaptiveportal server.

![![](http://opencaptiveportal.googlecode.com/svn/trunk/doc/OpenCaptivePortal-Software_small.png)](http://opencaptiveportal.googlecode.com/svn/trunk/doc/OpenCaptivePortal-Software.png)

The services are divided into "packages", but interact.
The following daemons must be installed and configured.

Table of contents:



# Install #

## Routing and iptables ##

The iptables have two functions:

  * Allow VPN connections to the Universities ([SWITCHconnect Classic](http://www.switch.ch/mobile/classic/))
  * If a user has selected a WISP (wlan Internet Service Provider) by clicking on an iframe, the following packets will be marked in iptables (with the MARK target). With policy based routing we can then route these packets based on the MARK through a specific GRE tunnel. Each WISP has an own GRE tunnel.

The iptables are build with a template file within the django framework. When booting the machine, the hole iptables have to be created and applied. When a user clicks on an iframe to establish a connection to a WISP, only one iptables rule is added. This is done with django (see "landing page").


Relevant files for iptables:
> Template file:  templates/iptables-restore.tmpl
If you want specific firewall settings, you can easily edit the iptables template file.

> Script:         shell/make-iptables.py
Build the iptables-restore file. You can than apply this file with the iptables-restore command. You need this at startup of the GNU/Linux Box. Or if something bad happend.

> Rule updates:   helper/iptables.py
The iptables related (shell) code, which is used by django.


## SWITCHconnect Classic ##

SWITCHconnect Classic is a set of VPN server IP addresses. All members participating in this scope allow in their (wlan) network access to the other VPN server IP addresses.
At startup, we downlowd the newest set of IP addresses and apply it in the iptables rule set.

There a SWITCHconnect Classic user just need to start the VPN client and does not need to see the landing page or click on an iframe.


## Landing page ##

The landing page is not only the "website", which you can see at the beginning of your wlan session. It is also the middleware to configure the iptables and keeps track about the active users. The landing page is written in python with the [django framework](http://www.djangoproject.com/).

Here we will explain the different functions:

  * Landing page itself
Show the landing page and offers the API to the User to set the Routes to the WISPs.
> Landing page template:    templates/landingpage.htm  (as URL: /landingpage.php)
> Landing page python code: ocp/views.py
This is the welcome page for user, who are not using the VPN of the local University or SWITCHconnect Classic. On this landing page are the iframes of the WISPs.

> Add and delete routes:    ocp/views.py (as URL: /route.php and /back.php)
Add a route, if a user clicks on an iframe or deletes a route, if a user clicks on the back button on a website of an WISP. In fact, we are not "setting a route" but adding or deleting an iptables rule which sets or deletes a MARK in iptables.

As said earlier the landing page is made with the django framework. Django comes with a developement http server, but for productive use we will install a "real" http server. This http server will act as proxy between the http request from the users to the python django daemon. We will show how this can be accomplished with apache2 and fastcgi. So we habe the two parts

  * [installApache2](installApache2.md)
  * [installLandingpage](installLandingpage.md)


## XML RPC ##

Statusqueries for WISPs, like: "is there still client $foo" and "which MAC adress does $bar have".
> XML RPC Server: xml-rpc-server.py

This server needs ad user management, because each WISP has a user.
> Add User:       TODO


## DNS cache (here bind9) ##
There is a locale DNS cache. This is (unfortunately) needed because some provider need to resolve a domain name to private IP address space.

You can use whatever DNS resolver you want. We use bind9, for installation and appropriate installation see [installBind](installBind.md)


## Monitoring ##

### Munin ###

You can use munin for basic monitoring of the system heath.

  * [installMunin](installMunin.md)

### Ntop ###

We need a intelligent solution for monitoring the link utilizations, especially of the GRE tunnels to the WISPs. Mabye we can use ntop. Or MRTG. Think about it...


# Operations #

TO BE DONE