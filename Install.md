# Introduction #

This page roughly describes the necessary steps to setup an ocp box. There will be a VMware image available shortly. On this image, the work below has already be done. But you need to adjust many things in order to fit your network environment. So, please read this howto even if you install the VMware image.

Before you start, be aware that you need to get a server certificate.

# Base system #

Install Debian Lenny default server installation.

# Requirements #

We need and will install the following software versions:
  * python 2.5
  * django >= 1.0
  * postgresql >= 8.1
  * psycopg (postgresql interface for python)
  * dhcp3-server
  * openssl

# Prepare system #
## Install packages needed ##

```
aptitude install python-django postgresql python-psycopg dhcp3-server openssl vlan
aptitude install python2.5 python2.5-minimal
```

Check:
```
$ ls -la /usr/bin/python
lrwxrwxrwx 1 root root 9 2009-10-14 12:47 /usr/bin/python -> python2.5
```

## Configure networking ##

Edit /etc/network/interfaces and configure the VLAN ID you use to connect your wireless network:

```
# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).
auto lo eth0 eth1 eth1.901
iface lo inet loopback

iface eth0 inet static
	address 1.2.3.4
	netmask 255.255.255.0
	gateway 1.2.3.1
	# dns-* options are implemented by the resolvconf package, if installed
	dns-nameservers 1.3.4.5
	dns-search switch.ch

iface eth1 inet static

iface eth1.901 inet static
	address 1.1.0.1
	netmask 255.255.255.0
	
	up vconfig add eth1 901 || true
	
	down ip route flush dev eth1.901 || true
	down ip addr  flush dev eth1.901 || true
```
Do not forget to "turn on" routing on your system in /etc/sysctl.conf:
```
# Uncomment the next line to enable packet forwarding for IPv4
net.ipv4.conf.default.forwarding=1
# Uncomment the next line to enable packet forwarding for IPv6
net.ipv6.conf.default.forwarding=1
```

# Get a server certificate #

If you are a customer of SWITCH, you can get certificates from SWITCHpki: http://www.switch.ch/pki.

## How to create a certificate request ##

Edit `/etc/ssl/openssl.cnf` and fill in your data accordingly:

```
[ req ]
default_bits = 2048
prompt = no
encrypt_key = no
default_md = sha1
distinguished_name = dn
# optional, for requesting subjectAltName entries (uncomment to enable)
#req_extensions = req_ext

[ dn ]
C = CH
O = OFFICIAL_NAME_OF_YOUR_ORGANIZATION
# see https://www.switch.ch/pki/participants.html
# for the list of organizations participating in SWITCHpki
CN = FULLY_QUALIFIED_DOMAIN_NAME_OF_YOUR_SERVER

[ req_ext ]
# (make sure that req_extensions is uncommented above)
subjectAltName= DNS:FULLY_QUALIFIED_DOMAIN_NAME_OF_YOUR_SERVER, \
DNS:SECOND_FULLY_QUALIFIED_DOMAIN_NAME_OF_YOUR_SERVER, \
DNS:THIRD_FULLY_QUALIFIED_DOMAIN_NAME_OF_YOUR_SERVER
# ... add more if required
```

Then create the certificate request:

```
cd /etc/ssl
openssl req -new -config openssl.cnf -keyout private/key.pem -out request.csr
```

Put the content of `request.csr` into the form on https://switch.ch/pki/quovadis/request.html.

Install the received certificate to `/etc/ssl/`.

# Install Apache #

Follow [installApache2](installApache2.md). Then edit `/etc/apache2/site-enabled/landingpage` and replace the placeholders to fit your environment.

The user (e.g., `www-data`) which runs the webserver needs some sudo rights:
```
echo "
Cmnd_Alias PWLAN = /sbin/iptables, /sbin/ip, /sbin/iptables-restore
www-data        ALL=NOPASSWD:PWLAN
" >> /etc/sudoers
```

# Install BIND #

Follow [installBind](installBind.md).

# Install Munin #

Follow [installMunin](installMunin.md).

# Prepare the database #

First, create the database and set user passwords.

```
su postgres
psql
alter user postgres with encrypted password 'asdf';
create user pocp;
alter user pocp with encrypted password 'adsf';
create database pocp;
\q
```

Then edit `/etc/postgresql/8.3/main/pg_hba.conf` and replace "ident sameuser" by "password":

```
local   all         postgres                          password
local   all         all                               password
```

# Setup DHCP server #

Edit `/etc/dhcp3/dhcp.conf` and configure a subnet the nameserver and set the server to be authoritative:

```
ddns-update-style none;

option domain-name "domain.com";
option domain-name-servers <1.1.0.1>;

default-lease-time 600;
max-lease-time 7200;

authoritative;
log-facility local7;

subnet 1.1.0.0 netmask 255.255.255.0 {
  range 1.1.0.100 1.1.0.200;
  option routers 1.1.0.1;
}
```

Edit `edit /etc/default/dhcp3-server` and add the appropriate interface to the list of interfaces (replace 901 with your VLAN ID):

```
INTERFACES="eth1.901"
```

# Install ocp #

Check out the code from the subversion repository and copy it:

```
cd /usr/src/
svn checkout http://opencaptiveportal.googlecode.com/svn/trunk/ opencaptiveportal-readonly
cp -r /usr/src/opencaptiveportal/source/pocp /usr/local/
ln -s /usr/local/pocp /usr/lib/python2.5/site-packages/
```

Edit the ADMINS section in `/usr/local/pocp/settings.py`. Adjust the database connection settings (e.g. your password) just below:

```
[...]
ADMINS = (
    ('Foo Bar', 'foo.bar@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE   = 'postgresql'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME     = 'pocp'             # Or path to database file if using sqlite3.
DATABASE_USER     = 'pocp'             # Not used with sqlite3.
DATABASE_PASSWORD = 'asdf'         # Not used with sqlite3.
DATABASE_HOST     = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT     = ''             # Set to empty string for default. Not used with sqlite3.
[...]
```

## Setup database ##

```
cd /usr/local/pocp/
./manage.py syncdb
```

## Start services ##

Configure daemons to start automatically:
```
ln -s /usr/local/pocp/shell/init.d-landingpage /etc/init.d/pocp-landingpage
update-rc.d pocp-landingpage defaults
ln -s /usr/local/pocp/shell/init.d-xml-rpc /etc/init.d/pocp-xml-rpc
update-rc.d pocp-xml-rpc defaults
# Logrotate:
ln -s /usr/local/pocp/shell/logrotate /etc/logrotate.d/pocp
```

Start manually:
```
/etc/init.d/apache2 restart
/etc/init.d/pocp-landingpage start
/etc/init.d/pocp-xml-rpc start
```
