#!/usr/bin/env python3
# coding=utf-8
# Author: libin

import pexpect
import time
import getpass


def deliver_pubkey(host, password):
    errs = 'faild to deliver pubkey to {}.'.format(host)
    for i in range(3):
        child = pexpect.spawn('ssh-copy-id -i /root/.ssh/id_rsa.pub root@{}'.format(host))
        i = child.expect(['Are you sure you want to continue connecting', 'password: ', 'already exist', pexpect.EOF, pexpect.TIMEOUT])
        # print(i)
        # print(child.after)
        if i == 0:
            child.sendline('yes')
            i = child.expect(['password: ', 'already exist', pexpect.EOF, pexpect.TIMEOUT])
            if i == 0:
                child.sendline(password)
                i = child.expect(['you wanted were added', pexpect.EOF, pexpect.TIMEOUT])
                if i == 0:
                    return
                else:
                    break
            elif i == 1:
                return
            else:
                break
        elif i == 1:
            child.sendline(password)
            i = child.expect(['you wanted were added', pexpect.EOF, pexpect.TIMEOUT])
            if i == 0:
                return
            else:
                break
        elif i == 2:
            return
        else:
            time.sleep(10)
    return errs


if __name__ == '__main__':
    host = input('请输入ip：')
    password = getpass.getpass('请输入密码：')
    errs = deliver_pubkey(host, password)
    print(errs)