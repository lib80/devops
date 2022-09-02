#!/usr/bin/env python3
#author: libin
import sys
import json
import requests


def get_token(corpid, secret):
    params = {'corpid': corpid, 'corpsecret': secret}
    res = requests.get(url='https://qyapi.weixin.qq.com/cgi-bin/gettoken', params=params)
    access_token = res.json().get('access_token')
    return access_token if access_token else print('auth fail.')


def send_message(access_token, touser, message):
    data = json.dumps({
        'touser': touser,
        'toparty': 1,
        'msgtype': 'text',
        'agentid': 1000010,
        'text': {
            'content': message
        },
        "safe": 0})
    send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}'.format(access_token)
    requests.post(url=send_url, data=data)


if __name__ == '__main__':
    corpid = ''
    secret = ''
    access_token = get_token(corpid, secret)
    if access_token:
        send_message(access_token, sys.argv[1], sys.argv[3])
