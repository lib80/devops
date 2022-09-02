#!/bin/bash

if [ -e /usr/local/mysql ];then
    echo 'The mysql already exists.'
    exit 1
fi

version="${1:-x.x.x}"

yum -y install libaio
useradd -r -s /bin/false mysql
mkdir -p /data/mysqldata
chown -R mysql.mysql /data/mysqldata/

tar xf /usr/local/src/mysql-"$version"-linux-glibc2.12-x86_64.tar.gz -C /usr/local/
cd /usr/local/
mv mysql-"$version"-linux-glibc2.12-x86_64 mysql-"$version"
mkdir mysql-"$version"/conf
ln -s mysql-"$version"/ mysql
echo 'export PATH=/usr/local/mysql/bin:$PATH' > /etc/profile.d/mysql.sh
echo '/usr/local/mysql/lib' > /etc/ld.so.conf.d/mysql.conf
ldconfig

systemctl enable mysqld.service

# mysqld --initialize-insecure --user=mysql --datadir=/data/mysqldata
