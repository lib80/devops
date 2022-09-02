#!/usr/bin/env python3
# coding=utf-8
# Author: libin

import string
import random
import itertools


def mkpasswd(length=16, letter=8, digit=4):
    letters_ = string.ascii_letters
    digits_ = string.digits
    salt = '!@#%^_'

    char_seq = list(
        itertools.chain(
            (random.choice(letters_) for _ in range(letter)),
            (random.choice(digits_) for _ in range(digit)),
            (random.choice(salt) for _ in range(length - letter - digit))
        )
    )
    return ''.join(random.sample(char_seq, len(char_seq)))


if __name__ == '__main__':
    password = mkpasswd()
    print(password)
