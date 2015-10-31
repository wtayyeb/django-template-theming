# -*- coding:utf-8 -*-
'''
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

from appconf.base import AppConf

import theming


class _AppConf(AppConf):
    VERSION = theming.__version__
    ROOT = 'themes'


    class Meta:
        prefix			 = "THEMING"  # explicit

