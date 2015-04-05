Install and configure Bind9.

## config ##

Install bind9
```
apt-get install bind9
cd /etc/bind/
```

Add to named.conf.options (so that the munin-plugin will work):
```
statistics-file "/var/run/bind/run/named.stats";
```

Add to named.conf:
```
include "/etc/bind/named.conf.acl";
include "/etc/bind/named.conf.logging";
```

Create logging config file:
```
echo '
logging {
    channel logfile {
        file "/var/log/named.log";
        print-category yes;
        print-severity yes;
        print-time yes;
    };

    category default { 
        logfile; default_debug; 
    };

    category lame-servers { 
        null; 
    };
};
' > named.conf.logging
```

Create ACL config gile:
```
echo '
acl wlan {
    10.1.2.0/24; # TODO: Enter your WLan network here, only from this network are DNS queries allowed
};
' > named.conf.acl
```

Logrotate:
```
echo '
/var/log/named.log {
  daily
  missingok
  rotate 7
  compress
  delaycompress
  notifempty
  create 640 bind bind
  postrotate
    if [ -f /var/run/bind/run/named.pid ]; then
      /etc/init.d/bind9 restart > /dev/null
    fi
  endscript
}
' > /etc/logrotate.d/bind
```


Create zones file, etc.:
```
mkdir zones

echo '
zone "pwlan-swisscom-mobile.ch" {
        type    master;
        file    "pwlan-swisscom-mobile.ch";
        allow-query { localhost; wlan; };
};
' >> named.conf.local

echo '
$TTL 86400
@               IN              SOA     dns.pwlan-swisscom-mobile.ch. CHANGEME.example.com. (
                                        2;      serial
                                        10800;  refresh (3h)
                                        3600;   retry (1h)
                                        604800; expire (1 week)
                                        86400;  ttl (1d)
                                        )

                                NS      dns

dns             IN              A       0.0.0.0
www             IN              A       10.192.24.20
' >> zones/pwlan-swisscom-mobile.ch

# Change in named.conf.options the directory:
# -> directory "/etc/bind/zones";

# Reload Bind.
/etc/init.d/bind9 restart
```


## checks ##

```
host www.pwlan-swisscom-mobile.ch localhost 
# ...
# www.pwlan-swisscom-mobile.ch has address 10.192.24.20

# Check a host, so that the resolver has to do a DNS lookup:
host www.switch.ch localhost 
# ...
# www.switch.ch is an alias for oreius.switch.ch.
# oreius.switch.ch has address 130.59.138.34
# oreius.switch.ch has IPv6 address 2001:620:0:1b::b
```
