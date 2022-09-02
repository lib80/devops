#!/usr/bin/env python3
#author: libin
"""该脚本用于统计异常日志信息并推送给云之家机器人"""

import glob
import datetime
import json
import sys
import re
import logging
import requests
from apscheduler.schedulers.blocking import BlockingScheduler


def analyse(log_file_name_prefix, output_file, logger, receiver):
    yestoday_str = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    yestoday_log_file_name_prefix = '{}.{}'.format(log_file_name_prefix, yestoday_str)
    log_file_paths = glob.glob('{}*.log'.format(yestoday_log_file_name_prefix))
    if not log_file_paths:
        msg = '{}: 目标日志文件不存在\n'.format(yestoday_log_file_name_prefix)
        logger.error(msg)
        receiver.fire(msg)
        sys.exit(1)

    temp_dict = {}
    for file in log_file_paths:
        with open(file, encoding='utf-8', mode='r') as f:
            for line in f:
                if 'Msg: ' in line:
                    field_v = line.split('Msg: ')[-1].rstrip('\n')
                    if len(field_v) >= 100:
                        field_v = '{}...'.format(field_v[0:50])
                    if temp_dict.get(field_v):
                        temp_dict[field_v] += 1
                    else:
                        temp_dict[field_v] = 1
    temp_tuple = sorted(temp_dict.items(), key=lambda x: x[1], reverse=True)  # 按值降序排列
    temp_list = []
    for item in temp_tuple:
        temp_list.append('{}: {}'.format(item[0], item[1]))
    msg = '[日志异常信息统计]\n{}\n日志: {}\n日期: {}\n'.format('\n'.join(temp_list), log_file_name_prefix, yestoday_str)
    with open(output_file, encoding='utf-8', mode='a') as f:
        f.write('{}\n'.format(msg))
    receiver.fire(msg)


class YunZhiJiaRobot:
    def __init__(self, webhook, at_names, logger):
        self.webhook = webhook
        self.at_names = at_names
        self.logger = logger
        self.info = {'content': ''}
        self.suffix_for_at = ''
        if at_names:
            self.suffix_for_at += '@' + '@'.join(at_names)

    def fire(self, msg):
        #self.info['content'] = msg.replace('java.lang', 'java_lang') + self.suffix_for_at
        self.info['content'] = re.sub('java\.(?P<type>io|lang)', 'java_\g<type>', msg) + self.suffix_for_at
        resp = requests.post(url=self.webhook, data=json.dumps(self.info), headers={'Content-Type': 'application/json;;charset=utf-8'})
        if resp.status_code != 200:
            self.logger.error(resp.text)


if __name__ == '__main__':
    log_file_name_prefix = 'someapp.error.log'
    output_file = '/somepath/log_statistic.txt'
    webhook = 'https://www.yunzhijia.com/gateway/robot/webhook/send?yzjtype=0&yzjtoken=xxx'
    at_names = ['xxx', 'xxx']

    # 创建日志记录器
    logger = logging.getLogger()
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.WARNING)

    # 创建通知接收器
    receiver = YunZhiJiaRobot(webhook=webhook, at_names=at_names, logger=logger)

    #analyse(log_file_name_prefix, output_file, logger, receiver)

    # 创建定时任务
    sched = BlockingScheduler()
    sched.add_job(analyse, trigger='cron', args=[log_file_name_prefix, output_file, logger, receiver], timezone='Asia/Shanghai', hour=10)
    sched.start()
