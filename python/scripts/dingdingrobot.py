#!/usr/bin/env python3
# author:libin
"""钉钉报警"""
import sys
import json
import requests
import time
import hmac
import hashlib
import base64
import urllib.parse


class Receiver:
    def __init__(self, access_token, secret, at_mobiles):
        self.access_token = access_token
        self.secret = secret
        self.at_mobiles = at_mobiles

    def fire(self, text):
        # 获取动态webhook
        timestamp = str(round(time.time() * 1000))
        secret_enc = self.secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        webhook = 'https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}'.format(self.access_token,
                                                                                                     timestamp, sign)
        # 构建数据
        text_dic = {
            "msgtype": "text",
            "at": {
                "atMobiles": self.at_mobiles,
                "isAtAll": False
            },
            "text": {
                "content": text
            }
        }
        # 发送请求
        resp = requests.post(url=webhook, data=json.dumps(text_dic),
                             headers={'Content-Type': 'application/json;charset=utf-8'})
        if resp.status_code != 200:
            print(resp.text)
        

if __name__ == '__main__':
    access_token = 'xxx'
    secret = 'xxx'
    at_mobiles = [133xxx]
    
    receiver = Receiver(access_token, secret, at_mobiles)
    text = sys.argv[1]
    receiver.fire(text)