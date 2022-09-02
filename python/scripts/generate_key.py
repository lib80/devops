#!/usr/bin/env python3
# coding=utf-8
# Author: libin

import pexpect


def generate_key():
    child = pexpect.spawn('ssh-keygen -t rsa -f /root/.ssh/id_rsa')
    i = child.expect(['Enter passphrase', 'Overwrite (y/n)?'])
    if i == 0:
        child.sendline()
        child.expect('passphrase again')
        child.sendline()
        i = child.expect(pexpect.EOF)
        res = 'The key has been generated.'
    elif i == 1:
        child.sendline('n')
        i = child.expect(pexpect.EOF)
        res = 'It already exists.'
    return res


if __name__ == '__main__':
    res = generate_key()
    print(res)
