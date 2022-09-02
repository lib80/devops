#!/bin/bash

if [ -e /usr/local/kafka ];then
    echo 'The kafka already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/kafka_"$version".tgz -C /usr/local/
cd /usr/local/
ln -s kafka_"$version"/ kafka
cd kafka/config/
sed -i '/^log.dirs/c log.dirs=/data/kafka/logs' server.properties
mkdir -p /data/kafka/logs
chown -R nobody.nobody /data/kafka/ /usr/local/kafka_"$version"/

systemctl enable kafka.service
