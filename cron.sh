#!/bin/sh
django=`nmap -p80 0.0.0.0|grep open`

if [ "${django}" == "" ]; then
   sudo python /opt/www/main/manage.py runserver 0.0.0.0:80
fi

live=`nmap -p8069 5.196.13.181|grep open`
if [ "${live}" == "" ]; then
   sudo service odoo-live start
fi

test=`nmap -p8070  5.196.13.181|grep open`
if [ "${test}" == "" ]; then
   sudo service odoo-11 start
fi

special=`nmap -p9089  5.196.13.181|grep open`
if [ "${special}" == "" ]; then
   sudo service odoo-special start
fi
 
