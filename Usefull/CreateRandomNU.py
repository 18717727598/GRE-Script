#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'bruce.jikun@gmail.com'


"""
Created by PyCharm.
File:               CreateRandomNU.py
Create Date:        2018/12/06
Modify Date:        Wed Jun  5 16:26:12 CST 2019
Note:
    Usage:
    Using user as you want in Linux/Windows system.
    The python module '' and '' is required, using pip
    install them.
    ```
    pip install *.py
    ```
    On OSX this function requires root privileges.
    # python PyZabbixApiBasicGetUseage.py

    Elapsed time: 0.0104579925537 seconds.
    #
 """


import random

import string


longnu = input('How long of number? I propose no less than 18,and default value is 18: ')
neednu = input('How many numbers do you want ? and default value is 1 ! ')
pun = '!$%&+,-.:;<=>?@[\\]^_'

newnu = 1

if longnu == '':
    longnu = 18
    if neednu == '':
        salt = ''.join(random.sample(string.ascii_letters + string.digits + pun, int(longnu)))
        print(salt)
    else:
        while int(newnu) <= int(neednu):
            salt = ''.join(random.sample(string.ascii_letters + string.digits + pun, int(longnu)))
            print(salt)
            newnu += 1
else:
    if neednu == '':
        salt = ''.join(random.sample(string.ascii_letters + string.digits + pun, int(longnu)))
        print(salt)
    else:
        while int(newnu) <= int(neednu):
            salt = ''.join(random.sample(string.ascii_letters + string.digits + pun, int(longnu)))
            print(salt)
            newnu += 1
