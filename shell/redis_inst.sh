#!/bin/bash

if [ -e /usr/local/redis ];then
    echo 'The redis already exists.'
    exit 1
fi

version="${1:-x.x.x}"
useradd -d /data/redisdata -s /sbin/nologin redis
cd /usr/local/src/
tar xf redis-"$version".tar.gz
cd redis-"$version"
make && make PREFIX=/usr/local/redis-"$version" install
mkdir /usr/local/redis-"$version"/conf
cp redis.conf /usr/local/redis-"$version"/conf/
cd /usr/local/
ln -s redis-"$version" redis
echo 'export PATH=/usr/local/redis/bin:$PATH' > /etc/profile.d/redis.sh
