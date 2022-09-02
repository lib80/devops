#!/bin/bash

if [ -e /usr/local/grafana ];then
    echo 'The grafana already exists.'
    exit 1
fi

version="${1:-x.x.x}"
tar xf /usr/local/src/grafana-"$version".linux-amd64.tar.gz -C /usr/local/
cd /usr/local/
ln -s grafana-"$version"/ grafana
chown -R nobody.nobody grafana-"$version"/

systemctl enable grafana.service
