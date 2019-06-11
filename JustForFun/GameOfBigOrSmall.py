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

    totalmoney = int(1000)
    while totalmoney >= 0:

        point1 = random.randrange(1, 7)
        point2 = random.randrange(1, 7)
        point3 = random.randrange(1, 7)

        a_list = [point1, point2, point3]
        result = sum(a_list)


        print('<<<<<<<< GAME STARTS! >>>>>>>>')
        playerguess = input('Big or Small ?')
        wannabet = input('How much you wanna bet ? ')

        if 3 <= result <= 10:
            realresult = 'Small'
        else:
            realresult = 'Big'

        if playerguess == realresult:
            totalmoney = int(totalmoney) + int(wannabet)
            print('The point are {}, You Win!!!'.format(a_list))
            print('You gained {},You have {} now!'.format(wannabet, totalmoney))
        else:
            totalmoney = int(totalmoney) - int(wannabet)
            print('The point are {}, You Lose!!!'.format(a_list))
            print('You lost {}, You have {} now!'.format(wannabet, totalmoney))
            if totalmoney == 0:
                print('GAME OVER!')
                exit(0)


if __name__ == '__main__':
    main()