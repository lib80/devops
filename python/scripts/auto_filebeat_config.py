#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author: libin
# 该脚本用于自动探测主机上是否存在指定日志（nginx访问日志、mysql慢日志、应用日志）并自动生成相应filebeat配置文件
import os
import re
import subprocess
import socket

config_li = []

# 获取本机ip
ip = socket.gethostbyname(socket.gethostname())

# nginx访问日志收集配置
nginx_access_log = '/somepath/access.log'
nginx_config = f"""
- type: log
  paths:
    - {nginx_access_log}
  #tail_files: true
  fields:
    type: nginx-access
  fields_under_root: true
  max_bytes: 1048576
"""
cmd = 'ps -ef | grep nginx | grep -v grep | wc -l'
p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
res = int(p.stdout.strip())
if res and os.path.exists(nginx_access_log):
    config_li.append(nginx_config)


# 应用日志收集配置
mulpat = r'^\d{4}-\d{2}-\d{2}'
cmd = 'ls /somepath/*/app/*.log'
p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
if not p.returncode:
    res = p.stdout.strip()
    path_list = res.split('\n')
    app_dc = {}
    for pt in path_list:
        flag = True
        basename = os.path.basename(pt)
        for k in ['rpc', 'exception', 'bucket', 'shardIndex']:
            if k in basename:
                flag = False
                break
        if flag:
            app_name = basename.split('.log')[0]
            app_dc.setdefault(app_name, re.sub(r'_\d+.*?/', '*/', pt))

    for type, path in app_dc.items():
        app_config = f"""
- type: log
  paths:
    - {path}
  #tail_files: true
  multiline.pattern: '{mulpat}'
  multiline.negate: true
  multiline.match: after
  include_lines: ['java.net.SocketTimeoutException']
  fields:
    type: app-{type}
  fields_under_root: true
  max_bytes: 1048576
  tags: ["catalina"]
     """
        config_li.append(app_config)


# mysql慢日志收集配置
mysql_slow_log = '/somepath/mysql_slow.log'
mysql_config = f"""
- type: log
  paths:
    - {mysql_slow_log}
  #tail_files: true
  exclude_lines: ['^\# Time']
  multiline.pattern: '^\# Time|^\# User'
  multiline.negate: true
  multiline.match: after
  fields:
    type: mysql-slow
  fields_under_root: true
  max_bytes: 1048576
"""
cmd = 'ls /somepath/mysql_slow.log'
p = subprocess.run(cmd, shell=True, text=True, capture_output=True)
if not p.returncode:
    config_li.append(mysql_config)


front = "filebeat.inputs:\n"

topic = r'elk-%{[type]}'
rear = f"""
output.kafka:
  hosts: ["127.0.0.1:9092"]
  topic: {topic}

#output.console:
#  pretty: true

processors:
  - drop_fields:
      fields: ["input", "log", "ecs", "host", "agent"]
  - add_fields:
      target: ""
      fields:
        node: {ip}

max_procs: 1
queue.mem:
  events: 1024
  flush.min_events: 512
  flush.timeout: 3s
"""

if config_li:
    with open('/somepath/filebeat.yml', 'w') as f:
        f.write(front)
        for sec in config_li:
            f.write(sec)
        f.write(rear)
