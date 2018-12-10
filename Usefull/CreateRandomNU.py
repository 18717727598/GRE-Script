#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'bruce.jikun@gmail.com'


"""
Created by PyCharm.
File:               CreateRandomNU.py
Create Date:        2018/12/06
Create Time:        15:11
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


longnu = raw_input('How long of number? I propose no less than 15: ')
neednu = raw_input('How many numbers do you want? ')
pun = '!$%&+,-.:;<=>?@[\\]^_'

newnu = 1
while int(newnu) <= int(neednu):
    salt = ''.join(random.sample(string.ascii_letters + string.digits + pun, int(longnu)))
    print salt
    newnu += 1