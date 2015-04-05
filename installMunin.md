Install munin to get some statistics.

You need a webserver, so that you can see the statistics. Read [installApache2](installApache2.md)

## install ##

```
apt-get install munin munin-node
```


## config ##

Normally it works out of the box. You want to add the bind_plugin, which you can find in the subversion repository under munin/plugins/bind_ (just copy it "as is" in the directory /etc/munin/plugins/ and restart the munin node daemon with /etc/init.d/munin-node restart).


## checks ##

Visit the URL:
> /munin
