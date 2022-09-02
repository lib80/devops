#!/bin/bash

if [ -e /usr/local/nginx ]; then
    echo 'The nginx already exists.'
    exit 1
fi

version="${1:-x.x.x}"

yum -y install pcre-devel openssl-devel zlib-devel
cd /usr/local/src/
tar xf nginx-"$version".tar.gz
tar xf nginx-module-vts-0.1.18.tar.gz
cd nginx-"$version"
./configure --prefix=/usr/local/nginx --pid-path=/var/run/nginx.pid --error-log-path=/data/nginxlog/error.log --http-log-path=/data/nginxlog/access.log --with-http_gzip_static_module --with-http_stub_status_module --with-http_ssl_module --with-pcre --with-file-aio --with-http_realip_module --with-stream --with-stream_ssl_module --add-module=/usr/local/src/nginx-module-vts-0.1.18
make && make install
mkdir -p /usr/local/nginx/ssl
echo 'export PATH=/usr/local/nginx/sbin:$PATH' > /etc/profile.d/nginx.sh

systemctl enable nginx.service