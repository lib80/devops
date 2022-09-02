#!/bin/bash

if [ -e /usr/local/redis_exporter ];then
    echo 'The redis_exporter already exists.'
    exit 1
fi

version="${1:-x.x.x}"
tar xf /usr/local/src/redis_exporter-"$version".linux-amd64.tar.gz -C /usr/local/
cd /usr/local/
mv redis_exporter-"$version".linux-amd64/ redis_exporter-"$version"
ln -s redis_exporter-"$version"/ redis_exporter
chown -R nobody.nobody redis_exporter-"$version"/

systemctl enable redis_exporter.service
