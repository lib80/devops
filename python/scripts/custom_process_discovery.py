#!/usr/bin/env python3
# author: libin
import os
import re
import json


def get_app_process(app_list):
    pattern = re.compile(r'^(some|other)_')
    for app in app_list:
        ls_dir = os.listdir('/usr/local/{}'.format(app))
        for path in ls_dir:
            if pattern.match(path):
                process_list.append({'{#CUSTOM}': path})


def get_other_process(other_list):
    for other in other_list:
        process_list.append({'{#CUSTOM}': other})


if __name__ == '__main__':
    app_list = []
    other_list = [
        'backup-1.0.jar'
    ]
    process_list = []
    if app_list: get_app_process(app_list)
    if other_list: get_other_process(other_list)
    res = json.dumps({'data': process_list}, indent=2)
    print(res)
