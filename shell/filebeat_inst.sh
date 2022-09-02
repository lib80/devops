#!/bin/bash

if [ -e /usr/local/filebeat ];then
    echo 'The filebeat already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/filebeat-"$version"-linux-x86_64.tar.gz -C /usr/local/
cd /usr/local/
mv filebeat-"$version"-linux-x86_64 filebeat-"$version"
ln -s filebeat-"$version"/ filebeat
cd filebeat/
mv filebeat.yml filebeat.yml.back
mkdir -p /data/filebeat/{data,logs}
chown -R nobody.nobody /data/filebeat/ /usr/local/filebeat-"$version"/

systemctl enable filebeat.service
