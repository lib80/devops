#!/bin/bash

if [ -e /usr/local/memcached_exporter ];then
    echo 'The memcached_exporter already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/memcached_exporter-"$version".linux-amd64.tar.gz -C /usr/local/
cd /usr/local/
mv memcached_exporter-"$version".linux-amd64 memcached_exporter-"$version"
ln -s memcached_exporter-"$version"/ memcached_exporter
chown -R nobody.nobody memcached_exporter-"$version"/

systemctl enable memcached_exporter.service
