#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# Author: libin
"""用作kibana sentinl的webhook"""
from flask import Flask, request
import requests
import json

app = Flask(__name__)

CORPID = 'xxx'
CORPSECRET = 'xxx'
AGENTID = 'xxx'

@app.route('/alert', methods=['POST'])
def alert():
    
    content = request.data.decode('utf-8')
    if content:
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        params = {'corpid': CORPID, 'corpsecret': CORPSECRET}
        resp = requests.get(url=url, params=params)
        access_token = resp.json().get('access_token')
        api = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
        msg = {'touser': '@all', 'toparty': '1', 'msgtype': 'text', 'agentid': AGENTID,
               'text': {'content': content}, 'safe': '0'}
        resp = requests.post(url=api, json=msg, headers={'Content-Type': 'application/json;charset=utf-8'})
        res = resp.text
    else:
        res = 'empty content.'
    return res


if __name__ == '__main__':
    app.run()
