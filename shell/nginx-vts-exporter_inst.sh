#!/bin/bash

if [ -e /usr/local/nginx-vts-exporter ];then
    echo 'The nginx-vts-exporter already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/nginx-vts-exporter-"$version".linux-amd64.tar.gz -C /usr/local/
cd /usr/local/
mv nginx-vts-exporter-"$version".linux-amd64 nginx-vts-exporter-"$version"
ln -s nginx-vts-exporter-"$version" nginx-vts-exporter
chown -R nobody.nobody nginx-vts-exporter-"$version"/

#systemctl enable nginx-vts-exporter.service
