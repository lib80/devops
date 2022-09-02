#!/bin/bash

if [ -e /usr/local/kibana ]; then
    echo 'The kibana already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/kibana-"$version"-linux-x86_64.tar.gz -C /usr/local/
cd /usr/local/
mv kibana-"$version"-linux-x86_64 kibana-"$version"
ln -s kibana-"$version"/ kibana

/usr/local/kibana/bin/kibana-plugin install file:///usr/local/src/sentinl-v"$version".zip
chown -R nobody.nobody kibana-"$version"/

systemctl enable kibana.service
