#!/bin/bash

if [ -e /usr/local/zabbix ];then
    echo 'The zabbix already exists.'
    exit 1
fi

version="${1:-x.x.x}"

useradd -d /var/lib/zabbix -s /sbin/nologin zabbix
cd /usr/local/src/
tar xf zabbix-"$version".tar.gz
cd zabbix-"$version"/
./configure --prefix=/usr/local/zabbix-"$version" --enable-agent
make install
cd /usr/local/
ln -s zabbix-"$version"/ zabbix
cd zabbix/etc/
mv zabbix_agentd.conf zabbix_agentd.conf.back
cat > zabbix_agentd.conf <<- EOF
LogFile=/tmp/zabbix_agentd.log
Server=192.168.1.1
ServerActive=192.168.1.1
HostMetadataItem=system.uname
Include=/usr/local/zabbix/etc/zabbix_agentd.conf.d/*.conf
EOF

systemctl enable zabbix-agent
