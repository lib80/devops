#!/bin/bash

if [ -e /usr/local/openssl ];then
    echo 'The openssl already exists.'
    exit 1
fi

version="${1:-x.x.x}"

cd /usr/local/src/
tar xf openssl-"$version".tar.gz
cd openssl-"$version"/
./config --prefix=/usr/local/openssl
make && make install
echo '/usr/local/openssl/lib' > /etc/ld.so.conf.d/openssl.conf
ldconfig
echo 'export PATH=/usr/local/openssl/bin:$PATH' > /etc/profile.d/openssl.sh