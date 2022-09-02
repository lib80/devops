#!/usr/bin/env python3
"""该脚本用于统计每日的PV、UV、热资源及失败请求的比例"""
import datetime
from collections import Counter


ips = []
c = Counter()
fail_count = 0

with open('/somepath/access.log') as f:
    for line in f:
        temp = line.split()
        ips.append(temp[0])
        c[temp[6]] += 1
        if int(temp[8]) > 400:
            fail_count += 1

PV = len(ips)
UV = len(set(ips))
hot_resources = c.most_common(5)
fail_percent = '{:.2f}%'.format(fail_count * 100.0 / PV)
today = datetime.date.today()

with open('/somepath/statistics_for_ngx.txt', 'a', encoding='utf-8') as f:
    print(today, PV, UV, fail_percent, hot_resources, file=f)