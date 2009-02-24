#!/usr/bin/make -f 
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

# ONLY USE TABs IN ACTION LINES!
# TODO:
# - link landingpage & Co to /var/www

OPTS := -O2
INSTALL = install -c 

SED = sed

pkg_name = opencaptiveportal

CONFDIR  = etc/$(pkg_name)
SHAREDIR = var/lib/$(pkg_name)
LIBDIR   = usr/lib/$(pkg_name)
WWWDIR   = var/www

WWWUSER = www-data

# all: install-db.tmpl iptables.tmpl make-iptables.py manage-route.py back.php \
# 	landingpage.php route.php xml-rpc-server.py add-user.py install-db.sh

#all:

#opencaptiveportal: 
all:
	for i in *.in; do \
		e=`echo $$i | $(SED) 's/.in$$//'`; \
		cp $$i $$e; \
		$(SED) -i -e 's#@CONFDIR@#/$(CONFDIR)#'   $$e; \
		$(SED) -i -e 's#@SHAREDIR@#/$(SHAREDIR)#' $$e; \
		$(SED) -i -e 's#@LIBDIR@#/$(LIBDIR)#'     $$e; \
		$(SED) -i -e 's#@WWWDIR@#/$(WWWDIR)#'      $$e; \
		$(SED) -i -e 's#@WWWUSER@#$(WWWUSER)#'    $$e; \
	done

install: 
	$(INSTALL) -m  755                   -d $(DESTDIR)/$(CONFDIR)/ 
	$(INSTALL) -m 0644 install-db.tmpl      $(DESTDIR)/$(CONFDIR)/install-db.tmpl 
	$(INSTALL) -m 0644 iptables.tmpl        $(DESTDIR)/$(CONFDIR)/iptables.tmpl 
	$(INSTALL) -o $(WWWUSER)             -d $(DESTDIR)/$(SHAREDIR)/ 
	$(INSTALL)                           -d $(DESTDIR)/$(LIBDIR)/iptables/ 
	$(INSTALL) -m 0755 make-iptables.py     $(DESTDIR)/$(LIBDIR)/iptables/make-iptables.py 
	$(INSTALL) -m 0755 manage-route.py      $(DESTDIR)/$(LIBDIR)/iptables/manage-route.py 
	$(INSTALL)                           -d $(DESTDIR)/$(LIBDIR)/htdocs/ 
	$(INSTALL) -m 0644 back.php             $(DESTDIR)/$(LIBDIR)/htdocs/back.php 
	$(INSTALL) -m 0644 landingpage.php      $(DESTDIR)/$(LIBDIR)/htdocs/landingpage.php 
	$(INSTALL) -m 0644 route.php            $(DESTDIR)/$(LIBDIR)/htdocs/route.php 
	$(INSTALL)                           -d $(DESTDIR)/$(LIBDIR)/server/
	$(INSTALL) -m 0644 xml-rpc-server.py    $(DESTDIR)/$(LIBDIR)/server/xml-rpc-server.py 
	$(INSTALL) -m 0644 SecureXMLRPCServer.py  $(DESTDIR)/$(LIBDIR)/server/SecureXMLRPCServer.py
	$(INSTALL) -m 0755 add-user.py          $(DESTDIR)/$(LIBDIR)/server/add-user.py
	$(INSTALL) -m 0755 install-db.sh        $(DESTDIR)/$(LIBDIR)/server/install-db.sh

distclean: clean

clean: 
	for i in *.in; do \
		e=`echo $$i | $(SED) 's/.in$$//'`; \
		rm $$e; \
	done
	

uninstall:
	rm -rf  $(DESTDIR)/$(CONFDIR)/ \
	rm -rf  $(DESTDIR)/$(SHAREDIR)/ \
	rm -rf  $(DESTDIR)/$(LIBDIR)/

test:

gnu:


