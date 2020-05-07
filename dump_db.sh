#!/bin/sh

##########################################
## OpenERP Backup Script
##########################################
## Backuping bases and addons to local dir
##########################################

# Stop All needed services
/etc/init.d/odoo-live stop
/etc/init.d/odoo-11 stop
/etc/init.d/odoo-special stop
/etc/init.d/etherpad-lite stop

date=`date +"%Y%m%d"`
host=ftpback-rbx6-63.ovh.net
user=vps187083.ovh.net
pwd=vjGEvVaKTs

export PGPASSWORD=5ee72809c5ac1c810f71b30b99511962

# Dump DBs
for db in BNO_BG_v8 BNO_BG_v11 BNO_CR_v11 BNO_MD_v8 BNO_RO_v8 BNO_SE_v11 BNO_SE_v8 odoo11 HSP_UA_v8 etherpad_base ProjectA_i2
do
  filename="/var/pgdump/${db}_${date}.backup"
  pg_dump -i -h 127.0.0.1 -p 5432 -U postgres -E UTF-8 -F c -b -f $filename $db
  gzip $filename
done

  tar -zcvf /var/pgdump/addons-live_${date}.tar.gz /opt/odoo-live/addons/
  tar -zcvf /var/pgdump/addons-test_${date}.tar.gz /opt/odoo-test/addons/
  tar -zcvf /var/pgdump/addons-11_${date}.tar.gz /opt/odoo-11/addons/

# Start All needed services
/etc/init.d/odoo-live start
/etc/init.d/odoo-11 start
/etc/init.d/odoo-special start
/etc/init.d/etherpad-lite start

echo 'Complit'
exit 0
