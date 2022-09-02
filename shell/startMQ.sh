#!/bin/bash
#这个脚本用来启动rocketmq，先启动nameserver然后启动broker

#加载环境变量
source /etc/profile

cd /usr/local/rocketmq
#启动nameserver
echo "start mqnamesrv now ..."
nohup ./bin/mqnamesrv &
sleep 2
ps aux | grep -v grep | grep mqnamesrv
#启动broker
echo "start broker now ..."
nohup ./bin/mqbroker -c conf/broker.conf &
sleep 2
ps aux | grep -v grep | grep broker
