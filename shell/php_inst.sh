#!/bin/bash

if [ -e /usr/local/php ];then
    echo 'The php already exists.'
    exit 1
fi

version="${1:-x.x.x}"

yum -y install mariadb-libs libxml2-devel libjpeg-turbo-devel libpng-devel freetype-devel gd-devel
cd /usr/local/src/
tar xf php-"$version".tar.gz
cd php-"$version"/
./configure --prefix=/usr/local/php-"$version" --with-config-file-path=/usr/local/php-"$version"/etc --enable-fpm --enable-mysqlnd --with-mysqli=mysqlnd --with-pdo-mysql=mysqlnd --with-gd --with-png-dir --with-jpeg-dir --with-freetype-dir --enable-bcmath --with-libxml-dir --enable-sockets --enable-mbstring -with-gettext --enable-opcache --with-openssl
make && make install

cd /usr/local/
ln -s php-"$version"/ php
cd php/etc/
mv php-fpm.conf.default php-fpm.conf
sed -i '/php-fpm.pid/c pid = run/php-fpm.pid' php-fpm.conf
cp /usr/local/src/php-"$version"/php.ini-production ./php.ini
cd php-fpm.d/
mv www.conf.default www.conf

systemctl enable php-fpm.service
