#!/bin/bash

if [ -e /usr/local/elasticsearch ]; then
    echo 'The elasticsearch already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/elasticsearch-"$version".tar.gz -C /usr/local/
cd /usr/local/
ln -s elasticsearch-"$version"/ elasticsearch
useradd -d /data/esdata -s /sbin/nologin es
chown -R es.es elasticsearch*

cat >> /usr/local/elasticsearch/config/elasticsearch.yml <<- EOF 

http.port: 9200
network.host: 0.0.0.0
path.data: /somepath/data
path.logs: /somepath/logs
path.repo: ["/somepath/backup"]
EOF

echo 262144 > /proc/sys/vm/max_map_count
echo 'vm.max_map_count=262144' >> /etc/sysctl.d/99-sysctl.conf
sysctl -p

systemctl enable elasticsearch.service
