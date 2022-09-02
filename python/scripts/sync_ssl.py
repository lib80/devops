#!/usr/bin/env python3
# author: libin
"""该脚本用于从zookeeper同步ssl证书数据"""
import os
import sys
import time
import logging
import subprocess
from kazoo.client import KazooClient


zk_hosts = 'xxx:2181'
zk_user = 'xxx'
zk_password = 'xxx'
cert_zk_node = '/somepath/cert.pem'
key_zk_node = '/somepath/key.pem'
cert_file = '/somepath/www.cert.pem'
key_file = '/somepath/www.key.pem'
log_file = os.path.join(os.path.dirname(__file__), 'sync_ssl.log')

logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

zk = KazooClient(hosts=zk_hosts, auth_data=[('digest', f'{zk_user}:{zk_password}')])
zk.start()


def watch_and_sync(node, file):
    @zk.DataWatch(node)
    def watch_cert(data, stat, event):
        if event and event.type == 'CHANGED':
            # print('配置已改变')
            with open(file, 'wb') as f:
                f.write(data)
            logger.info('节点数据变更，已同步数据')
            p = subprocess.run('nginx -s reload', shell=True, text=True, capture_output=True)
            if p.returncode:
                logger.error(p.stderr)
                zk.stop()
                sys.exit(1)


watch_and_sync(cert_zk_node, cert_file)
watch_and_sync(key_zk_node, key_file)


while True:
    time.sleep(10)
