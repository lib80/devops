#!/bin/bash

if [ -e /usr/local/zabbix ];then
    echo 'The zabbix already exists.'
    exit 1
fi

version="${1:-x.x.x}"

yum -y install mariadb-devel net-snmp-devel libevent-devel libxml2-devel libcurl-devel
useradd -d /var/lib/zabbix -s /sbin/nologin zabbix

cd /usr/local/src/
tar xf zabbix-"$version".tar.gz
cd zabbix-"$version"/
./configure --prefix=/usr/local/zabbix-"$version" --enable-server --enable-agent --with-mysql --with-net-snmp --with-libcurl --with-libxml2 --with-openssl --enable-ipv6
make install
if [ -d /usr/local/nginx/html/ ]; then
    mkdir /usr/local/nginx/html/zabbix
    cp -r frontends/php/* /usr/local/nginx/html/zabbix/
fi
cd /usr/local/
ln -s zabbix-"$version"/ zabbix

systemctl enable zabbix-server
systemctl enable zabbix-agent
