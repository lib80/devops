#!/bin/bash

if [ -e /usr/local/jdk ];then
    echo 'The jdk already exists.'
    exit 1
fi

tar xf /usr/local/src/jdk-xxx-linux-x64.tar.gz -C /usr/local/
cd /usr/local/
ln -s jdkxxx/ jdk
echo -e 'export JAVA_HOME=/usr/local/jdk\nexport CLASSPATH=.:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar:$CLASSPATH\nexport PATH=$JAVA_HOME/bin:$PATH' > /etc/profile.d/jdk.sh
