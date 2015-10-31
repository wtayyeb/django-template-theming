# -*- coding:utf-8 -*-
'''
Created on Oct 31, 2015

@author: Wasim
'''

from appconf.base import AppConf

import theming


class _AppConf(AppConf):
    VERSION 			 = theming.__version__
    ROOT           = 'themes'  # Relative to settings.BASE_ROOT

    class Meta:
        prefix			 = "THEMING"  # explicit

