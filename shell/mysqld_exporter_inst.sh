#!/bin/bash

if [ -e /usr/local/mysqld_exporter ];then
    echo 'The mysqld_exporter already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/mysqld_exporter-"$version".linux-amd64.tar.gz -C /usr/local/
cd /usr/local/
mv mysqld_exporter-"$version".linux-amd64/ mysqld_exporter-"$version"
ln -s mysqld_exporter-"$version"/ mysqld_exporter
echo -e '[client]\nuser=\npassword=\nhost=\nport=' > /usr/local/mysqld_exporter/.my.cnf
chown -R nobody.nobody mysqld_exporter-"$version"/

#systemctl enable mysqld_exporter.service
