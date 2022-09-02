#!/bin/bash

if [ -e /usr/local/alertmanager ];then
    echo 'The alertmanager already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/alertmanager-"$version".linux-amd64.tar.gz -C /usr/local/
cd /usr/local/
mv alertmanager-"$version".linux-amd64 alertmanager-"$version"
ln -s alertmanager-"$version"/ alertmanager
mkdir -p /usr/local/alertmanager/templates
chown -R nobody.nobody /usr/local/alertmanager-"$version"/

systemctl enable alertmanager