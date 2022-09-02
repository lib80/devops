#!/usr/bin/env python3
# author: libin
import json


ports_list = [1111, 2222]
items_list = []
for port in ports_list:
    items_list.append({'{#ESPORT}': port})
res = json.dumps({'data': items_list}, indent=2)
print(res)
