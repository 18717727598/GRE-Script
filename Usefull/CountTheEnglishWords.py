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
 
import string

path = '/Users/pro/PycharmProjects/PythonResearch/WaldenPycharm.txt'

with open(path, 'r', encoding='utf8') as text:
    words = [raw_word.strip(string.punctuation).lower() for raw_word in text.read().split()]
    # dv = [ raw_word for raw_word in text.read().split()]
    # print(words)

    words_index = set(words)
    # print(words_index)

    count_dict = { index:words.count(index) for index in words_index}
    # print(count_dict)

    for word in sorted(count_dict, key=lambda x: count_dict[x], reverse=True):
        print('{} -- {} times'.format(word, count_dict[word]))