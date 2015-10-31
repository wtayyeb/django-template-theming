# -*- coding:utf-8 -*-
'''
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

from threading import local


_threadlocals = local()


def set_thread_variable(key, val):
	setattr(_threadlocals, key, val)


def get_thread_variable(key, default=None):
	return getattr(_threadlocals, key, default)
