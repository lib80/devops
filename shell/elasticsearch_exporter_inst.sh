#!/bin/bash

if [ -e /usr/local/elasticsearch_exporter ];then
    echo 'The elasticsearch_exporter already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/elasticsearch_exporter-"$version".linux-amd64.tar.gz -C /usr/local/
cd /usr/local/
mv elasticsearch_exporter-"$version".linux-amd64/ elasticsearch_exporter-"$version"
ln -s elasticsearch_exporter-"$version"/ elasticsearch_exporter
chown -R nobody.nobody elasticsearch_exporter-"$version"/

systemctl enable elasticsearch_exporter.service
