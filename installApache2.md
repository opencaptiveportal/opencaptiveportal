Install apache2 to serve as http server with fastcgi.

We need a http server between the django fastcgi server process and the users http requests.

You need **ssl certificates** for https (google can help you... or order from SWITCH pki at http://www.switch.ch/pki :))!

## install ##

```
apt-get install apache2 libapache2-mod-fastcgi python-flup
```


## config ##

Enable modules:
```
a2enmod rewrite
a2enmod ssl
a2enmod fastcgi
```

Site:
```
a2dissite default
cd /etc/apache2/sites-available
echo '
FastCGIExternalServer /var/www/fast_cgi/mysite.fcgi -socket /var/www/fast_cgi/mysite.sock -idle-timeout 60

<VirtualHost *:80>
        ServerAdmin CHANGEME@example.com

        ###RewriteEngine On
        ###RedirectMatch permanent ^/(.*)$ https://insert-fqdn-here/$1

        #DocumentRoot /var/www/landingpage.fast_cgi/
        DocumentRoot /var/www/fast_cgi/
        # Media files for admin interface:
        Alias /media /usr/share/python-support/python-django/django/contrib/admin/media
        RewriteEngine On
        RewriteRule ^/(media.*)$ /$1 [QSA,L,PT]
        RewriteRule ^/(.*)$ /mysite.fcgi/$1 [QSA,L]

        ErrorLog /var/log/apache2/landingpage_error.log
        CustomLog /var/log/apache2/landingpage_access.log combined
        LogLevel info
</VirtualHost>

<VirtualHost *:443>
        ServerAdmin CHANGEME@example.com

        #DocumentRoot /var/www/landingpage.fast_cgi/
        DocumentRoot /var/www/fast_cgi/
        # Media files for admin interface:
        Alias /media /usr/share/python-support/python-django/django/contrib/admin/media
        RewriteEngine On
        RewriteRule ^/(media.*)$ /$1 [QSA,L,PT]
        RewriteRule ^/(.*)$ /mysite.fcgi/$1 [QSA,L]

        ErrorLog /var/log/apache2/landingpage_error.log
        CustomLog /var/log/apache2/landingpage_access.log combined
        # Possible values include: debug, info, notice, warn, error, crit, alert, emerg.
        LogLevel info

        SSLEngine On
        SSLCertificateFile /etc/ssl/certs/CHANGEME.crt
        SSLCertificateKeyFile /etc/ssl/private/CHANGEME.key
</VirtualHost>
' >> landingpage

a2ensite landingpage


echo '
# For admin (phpmyadmin, etc.)

<VirtualHost 127.0.0.1:80>
        ServerName localhost
        ServerAdmin CHANGEME@example.com

        DocumentRoot /var/www/localhost/

        RewriteEngine on
        # http://www.kb.cert.org/vuls/id/867593
        RewriteCond %{REQUEST_METHOD} ^{TRACE|TRACK}
        RewriteRule .* - [F]

        <Directory /var/www/localhost/>
                Options Indexes FollowSymLinks MultiViews
                AllowOverride None
                Order deny,allow
                deny from all
                allow from 127.0.0.1/32
        </Directory>

        # For munin
        <Location /server-status>
                SetHandler server-status
                Order deny,allow
                Deny from all
                Allow from 127.0.0.1/32
        </Location>

</VirtualHost>
' > localhost

mkdir -p /var/www/localhost

a2ensite localhost

```

Restart Apache2.
```
/etc/init.d/apache2 restart
```

## checks ##

See the log files and check the website:
```
less /var/log/apache2/landingpage_access.log
less /var/log/apache2/landingpage_error.log
```