#!/usr/bin/env python3
#author: libin
"""用于从aws s3上下载csv文件并将其内容导入mysql"""
import os
import sys
import glob
import datetime
import subprocess
import logging
import zipfile
import pandas
import pymysql
from concurrent import futures
from multiprocessing import Lock
from apscheduler.schedulers.blocking import BlockingScheduler
import dingdingrobot


# 创建日志记录器
g_logger = logging.getLogger()
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler = logging.FileHandler('/usr/local/s3_to_mysql/s3_to_mysql.log')
file_handler.setFormatter(formatter)
g_logger.addHandler(file_handler)
g_logger.setLevel(logging.INFO)

# 创建钉钉告警接收器
ding_access_token = ''
ding_secret = ''
ding_at_mobiles = ['133xxx']
g_alert_receiver = dingdingrobot.Receiver(ding_access_token, ding_secret, ding_at_mobiles)

# mysql连接信息
mysql_info = {
    'host': '',
    'port': 3306,
    'user': '',
    'passwd': '',
    'db': '',
}


def report_err(msg: str):
    g_logger.error(msg)
    g_alert_receiver.fire(msg)
    sys.exit()


def normalize_csv(proj: str):
    g_logger.info(f'{proj}: starting to normalize csv file ...')
    cmd = f'/usr/local/s3_to_mysql/normalize_csv.sh {proj}.csv'
    p = subprocess.run(cmd, shell=True, capture_output=True)
    if p.returncode:
        report_err(f'{proj}: normalize csv file err.')


def download(proj: str):
    # 判断要下载的工程
    peak, date_s = None, None
    if proj in ['proj1', 'proj2']:
        peak = 'xxx'
        date_s = datetime.date(datetime.date.today().year, datetime.date.today().month, 19).strftime('%Y%m%d')
    elif proj in ['proj3', 'proj4']:
        peak = 'xxx'
        date_s = datetime.date.today().strftime('%Y%m%d')
    else:
        report_err(f'proj_name {proj} err.')

    # 下载
    g_logger.info('{}: starting to download files ...'.format(proj))
    cmd = f'/somepath/s3cmd get --force --recursive s3://{peak}/{proj}/{date_s}/'
    p = subprocess.run(cmd, shell=True, capture_output=True)
    ready_file = f'{proj}.ready'
    zip_file = f'{proj}.zip'
    if p.returncode or not (os.path.exists(ready_file) and os.path.exists(zip_file)):
        report_err(f'{proj}: download fail.')

    # 解压
    zf = zipfile.ZipFile(zip_file)
    zf.extractall()
    zf.close()

    # 处理某些csv文件可能存在的格式不规范的问题
    if proj == 'proj2':
        normalize_csv(proj)


def clean(proj: str):
    files_to_be_cleaned = glob.glob(f'*{proj}*')
    for file in files_to_be_cleaned:
        os.remove(file)


def handle_chunk(proj: str, primary_key: str, chunk: pandas.DataFrame):
    del_values = []
    insert_values = []
    cols = list(chunk.columns)
    cols.remove('operation')

    for index, row in chunk.iterrows():
        if row.get('operation') == 'D':
            del_values.append(row.get(primary_key))
        else:
            if row.get('operation'):
                del row['operation']
            for k, v in row.items():
                if pandas.isnull(v):
                    row[k] = None
            insert_values.append(tuple(row.values))

    my_conn = pymysql.connect(**mysql_info)
    cursor = my_conn.cursor()
    try:
        cursor.executemany(f'delete from {proj} where {primary_key}=%s', del_values)
        cursor.executemany(f'replace into {proj} ({", ".join(cols)}) values ({", ".join(["%s"] * len(cols))})', insert_values)
        my_conn.commit()
    finally:
        cursor.close()
        my_conn.close()

def export_to_mysql(proj):
    download(proj)

    if proj in ['proj1', 'proj2']:
        primary_key = 'xxx'
    elif proj == 'proj3':
        primary_key = 'id'
    else:
        primary_key = 'xxx'

    g_logger.info('{}: starting to export to mysql ...'.format(proj))
    data = pandas.read_csv(f'{proj}.csv', encoding='utf-8', sep=';', chunksize=100000)
    with futures.ProcessPoolExecutor() as executor:
        to_do = []
        for chunk in data:
            to_do.append(executor.submit(handle_chunk, proj, primary_key, chunk))
        for future in futures.as_completed(to_do):
            err = future.exception()
            if err:
                report_err(f'{proj}: {err}')
    g_logger.info('{}: success.'.format(proj))
    clean(proj)


if __name__ == '__main__':
    # export_to_mysql('proj1')
    # 创建定时任务
    sched = BlockingScheduler()
    sched.add_job(export_to_mysql, trigger='cron', args=['proj3'], timezone='Asia/Shanghai', hour=17)
    sched.add_job(export_to_mysql, trigger='cron', args=['proj4'], timezone='Asia/Shanghai', hour=18)
    sched.add_job(export_to_mysql, trigger='cron', args=['proj1'], timezone='Asia/Shanghai', day=20, hour=8)
    sched.add_job(export_to_mysql, trigger='cron', args=['proj2'], timezone='Asia/Shanghai', day=20, hour=22)
    sched.start()
