#!/usr/bin/env python3
#author: libin
import os
import re
import json


def get_apps_process(apps_list):
    pattern = re.compile(r'^(some|other)_')
    for app in apps_list:
        ls_dir = os.listdir('/usr/local/{}'.format(app))
        for path in ls_dir:
            if pattern.match(path):
                items_list.append({'{#CUSTOM}': path})


def get_others_process(others_list):
    for other in others_list:
        items_list.append({'{#CUSTOM}': other})


if __name__ == '__main__':
    apps_list = []
    others_list = [
        'backup-1.0.jar'
    ]
    items_list = []
    if apps_list: get_apps_process(apps_list)
    if others_list: get_others_process(others_list)
    res = json.dumps({'data': items_list}, indent=2)
    print(res)
