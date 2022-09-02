#!/bin/bash

if [ -e /usr/local/memcached ];then
    echo 'The memcached already exists.'
    exit 1
fi

version="${1:-x.x.x}"

yum -y install libevent-devel
useradd -d /var/run/memcached -s /sbin/nologin memcached

cd /usr/local/src/
tar xf memcached-"$version".tar.gz
cd memcached-"$version"/
./configure --prefix=/usr/local/memcached-"$version"
make && make install
cd /usr/local/
ln -s memcached-"$version"/ memcached

systemctl enable memcached.service
