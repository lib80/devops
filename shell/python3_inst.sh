#!/bin/bash

if [ -e /usr/local/python3 ];then
    echo 'The python3 already exists.'
    exit 1
fi

version="${1:-x.x.x}"

yum -y install bzip2-devel readline-devel openssl-devel sqlite-devel libffi-devel xz-devel python-backports-lzma
cd /usr/local/src/
tar xf Python-"$version".tar.xz
cd Python-"$version"/

# 如果openssl版本较低，且需要使用ssl模块，则应预先安装新版openssl，并修改Modules/Setup文件
cat >> Modules/Setup <<- 'EOF'
OPENSSL=/usr/local/openssl
_ssl _ssl.c \
    -I$(OPENSSL)/include -L$(OPENSSL)/lib \
    -lssl -lcrypto
EOF

./configure --prefix=/usr/local/python3
make && make install
echo 'export PATH=/usr/local/python3/bin:$PATH' > /etc/profile.d/python3.sh