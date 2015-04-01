# TODO #

Here are some notes about tasks which need to be done.
If you are interested, please get in contact with us and help us solve the problem.


Landing page:
  * (traffic) statistics (-> ntop ?)
  * In forward:filter is somewhere a "established -j ACCEPT", therefore, a User is not blocked directly after logout
  * After login the redirect does not work (-> User thinks I did not work?)
  * Do not bind cookies to URL (because the URL is not the URL of the landing page, but google.com, yahoo.com or whatever the user typed in)

Nice to have:
  * IPv6 cabability: The WISPs are maybe not able to offer IPv6 connectivity. In this case we can use teredo.
  * Possible TODOs:
    * Django has no IPv6 data type/field -> we have to expand the models.
    * Document, what is necessary for Teredo. And implement it.


# Known Bugs (we will not fix that ;)) #

  * In Internet Explorer the login box is to small


# Recently DONE #

  * init.d scripts are Debian style
  * GRE tunnels and ip configuration during start of landingpage daemon
  * ldap group
  * cleanup sessions and old routes
  * dhcp.php
  * XMP-RPC daemon start-up


# DONE #

XML RPC:
  * Start routine (the init.d script)

Landing page:
  * Get the listen ip address for xml-rpc from fqdn from ssl cert
  * Enable https (done ?)
  * Start routine (the init.d script)

Entire project:
  * Complete documentation of a new installation

Administrative:
  * Get mailing list ocp-dev (et) switch.ch
  * Describe TODO task, so that other person can do this tasks