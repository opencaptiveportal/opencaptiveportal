#!/bin/bash

# Wrapper for djangp python scripts (settings module)

LOG=/var/log/ocp/django-python.log

# Find out our working directory
THIS=$0
if [ ${THIS:0:1} != "/" ]; then
  THIS="$PWD/$0"
fi
cd `/usr/bin/dirname $THIS`

# log and execute
echo "`date`  $0  called  $1  start (pid $$)" >> $LOG

DJANGO_SETTINGS_MODULE="pocp.settings"  "$1"

echo "`date`  $0  called  $1  end   (pid $$)" >> $LOG

