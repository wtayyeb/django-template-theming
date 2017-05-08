# -*- coding:utf-8 -*-
"""
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
"""

from django.apps import AppConfig
from django.conf import settings

VERSION = (0, 7, 9)
__version__ = '.'.join((str(i) for i in VERSION))
default_app_config = __name__ + '.App'


class App(AppConfig):
    name = 'theming'

    class Defaults:
        THEMING_DEFAULT_THEME = 'default'
        THEMING_ROOT = 'themes'  # will append to BASE_DIR
        THEMING_URL = 'themes'  # will append to STATIC_URL

    def ready(self):
        self.configure()

    def configure(self):
        for name in (name for name in dir(self) if name.upper() == name):
            setattr(settings, name, getattr(self, name))

        for name in (name for name in dir(self.Defaults) if name.upper() == name):
            try:
                getattr(settings, name)
            except AttributeError:
                setattr(settings, name, getattr(self.Defaults, name))
