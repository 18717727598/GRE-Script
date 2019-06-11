#!/usr/bin/env python
# -*- coding: utf-8 -*-


__author__ = 'bruce.jikun@gmail.com'

"""
Created by PyCharm.
File:               xxx.py
Create Time:        Tue Jun  4 06:27:42 CST 2019
Note:
    Usage:
    Using user as you want in Linux/Windows system.
    The python module '' and '' is required, using pip
    install them.
    ```
    pip install psutil prettytable
    ```
    On OSX this function requires root privileges.
    # python portStatistics.py

    Elapsed time: 0.0104579925537 seconds.
    #
 """
 
import random


def main():

    usernumber = input('Please Enter Your Number? ')

    cn_mobile = ['134', '135', '136', '137', '138', '187', '158']
    cn_union = ['130', '131', '132', '155', '156']
    cn_telecom = ['133', '153', '180', '181', '189']
    headthree = usernumber[0:3]
    print(headthree)

    if len(usernumber) == 11:
        if headthree in cn_mobile:
            print('Operator : China Mobile')
            print('We are sending verification code via text to your phone: {}'.format(usernumber))
        elif headthree in cn_union:
            print('Operator : China Union')
            print('We are sending verification code via text to your phone: {}'.format(usernumber))
        elif headthree in cn_telecom:
            print('Operator : China Telecom')
            print('We are sending verification code via text to your phone: {}'.format(usernumber))
        else:
            print('No such a operator ! ')
    else:
        print('Invalid length,your number should be in 11 digits')




if __name__ == '__main__':
    main()