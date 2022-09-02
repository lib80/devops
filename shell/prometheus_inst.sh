#!/bin/bash

if [ -e /usr/local/prometheus ];then
    echo 'The prometheus already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/prometheus-"$version".linux-amd64.tar.gz -C /usr/local/
cd /usr/local/
mv prometheus-"$version".linux-amd64 prometheus-"$version"
ln -s prometheus-"$version"/ prometheus
mkdir -p /data/prometheus/{data,logs}
chown -R nobody.nobody /data/prometheus/ /usr/local/prometheus-"$version"/

systemctl enable prometheus
