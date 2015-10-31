# -*- coding:utf-8 -*-
'''
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

from appconf.base import AppConf


class _AppConf(AppConf):
    DEFAULT_THEME = 'default'
    ROOT = 'themes'  # will append to BASE_DIR
    URL = 'themes'  # will append to STATIC_URL

    class Meta:
        prefix			 = "THEMING"  # explicit

