#!/usr/bin/env python3
# author: libin
import smtplib
from email.message import EmailMessage

mail_host = 'smtp.exmail.qq.com'
mail_sender = ''
mail_license = ''
mail_receivers = ['']


def send_email(content: str, subject: str):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = mail_sender
    msg['To'] = ','.join(mail_receivers)
    s = smtplib.SMTP_SSL(mail_host)
    s.login(mail_sender, mail_license)
    s.send_message(msg)
    s.quit()


if __name__ == '__main__':
    send_email('ssl证书更新成功', '测试-ssl证书更新提醒')
