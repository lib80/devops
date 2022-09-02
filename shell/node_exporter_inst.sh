#!/bin/bash

if [ -e /usr/local/node_exporter ];then
    echo 'The node_exporter already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/node_exporter-"$version".linux-amd64.tar.gz -C /usr/local/
cd /usr/local/
mv node_exporter-"$version".linux-amd64/ node_exporter-"$version"
ln -s node_exporter-"$version"/ node_exporter
chown -R nobody.nobody node_exporter-"$version"/

systemctl enable node_exporter.service
