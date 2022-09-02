#!/usr/bin/env python3
# author: libin
"""该脚本用于建立定时任务适时更新ssl证书并更新数据到zookeeper"""
import os
import sys
import subprocess
import logging
from datetime import datetime, timedelta
from kazoo.client import KazooClient
from apscheduler.schedulers.blocking import BlockingScheduler
from send_email import send_email


project: str = 'xxx'
domain: str = 'xxx.com'
ssl_dir: str = '/somepath/ssl'
key_file: str = os.path.join(ssl_dir, f'{project}.key.pem')
cert_file: str = os.path.join(ssl_dir, f'{project}.cert.pem')
ahead_days: int = 5  # 到期时间前几天更新
log_file = os.path.join(os.path.dirname(__file__), 'update_ssl.log')

zk_hosts = '127.0.0.1:2181'
zk_user = ''
zk_password = ''
cert_zk_node = '/somepath/cert.pem'
key_zk_node = '/somepath/key.pem'

logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler = logging.FileHandler(log_file)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

scheduler = BlockingScheduler(timezone='Asia/Shanghai')


def report_err(msg: str):
    logger.error(msg)
    send_email(msg, f'{project} ssl证书更新提醒')
    sys.exit(1)


def update_zk_node():
    """更新数据到zookeeper节点"""
    zk = KazooClient(hosts=zk_hosts, auth_data=[('digest', f'{zk_user}:{zk_password}')])
    zk.start()
    zk.ensure_path(cert_zk_node)
    zk.ensure_path(key_zk_node)
    with open(cert_file, mode='rb') as f:
        cert_data = f.read()
    with open(key_file, mode='rb') as f:
        key_data = f.read()
    zk.set(cert_zk_node, cert_data)
    zk.set(key_zk_node, key_data)
    zk.stop()


def main():
    # 查看当前ssl证书到期时间
    p = subprocess.run(f'openssl x509 -in {cert_file} -noout -dates | grep "notAfter" | cut -d "=" -f2', shell=True,
                       text=True, capture_output=True)
    if p.returncode:
        report_err(f'查看当前ssl证书到期时间失败。{p.stderr.strip()}')
    cur_ssl_expire_time: datetime = datetime.strptime(p.stdout.strip(), '%b %d %H:%M:%S %Y GMT')

    if cur_ssl_expire_time - datetime.now() < timedelta(days=ahead_days + 2):
        # 备份证书
        p = subprocess.run(f'\\cp {cert_file} {cert_file}.old && \\cp {key_file} {key_file}.old', shell=True, text=True,
                           capture_output=True)
        if p.returncode:
            report_err(f'ssl证书备份失败。{p.stderr.strip()}')

        # 更新证书
        p = subprocess.run(
            f'/somepath/.acme.sh/acme.sh --renew --force -d \\*.{domain} && /somepath/.acme.sh/acme.sh --install-cert -d \\*.{domain} --key-file {key_file} --fullchain-file {cert_file}',
            shell=True, text=True, capture_output=True)
        if p.returncode:
            report_err(f'ssl证书更新失败。{p.stderr.strip()}')

        # 重载nginx配置
        p = subprocess.run('/somepath/sbin/nginx -s reload', shell=True, text=True, capture_output=True)
        if p.returncode:
            report_err(f'重载nginx配置失败。{p.stderr.strip()}')

        # 更新数据到zookeeper节点
        update_zk_node()

        # 查看新证书的到期时间
        p = subprocess.run(f'openssl x509 -in {cert_file} -noout -dates | grep "notAfter" | cut -d "=" -f2',
                           shell=True,
                           text=True, capture_output=True)
        if p.returncode:
            report_err(f'查看新ssl证书到期时间失败。{p.stderr.strip()}')
        new_ssl_expire_time_str: str = p.stdout.strip()
        new_ssl_expire_time: datetime = datetime.strptime(new_ssl_expire_time_str, '%b %d %H:%M:%S %Y GMT')
        msg = f'ssl证书更新成功，新证书的到期时间为 {new_ssl_expire_time_str}'
        logger.info(msg)
        send_email(msg, f'{project} ssl证书更新提醒')

        # 创建下次更新的定时任务
        scheduler.add_job(main, 'date', run_date=new_ssl_expire_time - timedelta(days=ahead_days))
    else:
        scheduler.add_job(main, 'date', run_date=cur_ssl_expire_time - timedelta(days=ahead_days))

if __name__ == '__main__':
    main()
    scheduler.start()