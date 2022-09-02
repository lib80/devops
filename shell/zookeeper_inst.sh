#!/bin/bash

if [ -e /usr/local/zookeeper ];then
    echo 'The zookeeper already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/zookeeper-"$version".tar.gz -C /usr/local/
cd /usr/local/
ln -s zookeeper-"$version"/ zookeeper
cd zookeeper/conf/
mv zoo_sample.cfg zoo.cfg
sed -i '/^dataDir/c dataDir=/data/zookeeper/data' zoo.cfg
mkdir -p /data/zookeeper/
chown -R nobody.nobody /data/zookeeper/ /usr/local/zookeeper-"$version"/
echo 'export PATH=/usr/local/zookeeper/bin:$PATH' > /etc/profile.d/zookeeper.sh

systemctl enable zookeeper.service
