# -*- coding:utf-8 -*-
'''
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

from appconf.base import AppConf


class _AppConf(AppConf):
    DEFAULT_THEME = 'default'
    ROOT = 'themes'

    class Meta:
        prefix			 = "THEMING"  # explicit

