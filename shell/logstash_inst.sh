#!/bin/bash

if [ -e /usr/local/logstash ];then
    echo 'The logstash already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/logstash-"$version".tar.gz -C /usr/local/
cd /usr/local/
ln -s logstash-"$version"/ logstash
chown -R nobody.nobody logstash-"$version"/

yum -y install haveged
systemctl enable --now haveged
systemctl enable logstash.service
