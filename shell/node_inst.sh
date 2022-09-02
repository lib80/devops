#!/bin/bash

if [ -e /usr/local/node ];then
    echo 'The node already exists.'
    exit 1
fi

version="${1:-x.x.x}"

tar xf /usr/local/src/node-"$version"-linux-x64.tar.xz -C /usr/local/
cd /usr/local/
mv node-"$version"-linux-x64 node-"$version"
ln -s node-"$version" node
/usr/local/node/bin/npm config set registry=https://registry.npm.taobao.org
/usr/local/node/bin/npm install -g cnpm
echo 'export PATH=/usr/local/node/bin:$PATH' > /etc/profile.d/node.sh