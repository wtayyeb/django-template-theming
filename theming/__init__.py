# -*- coding:utf-8 -*-
"""
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
"""
import logging
import os

from django.apps import AppConfig
from django.conf import settings

VERSION = (0, 7, 10)
__version__ = '.'.join((str(i) for i in VERSION))

default_app_config = __name__ + '.App'
logger = logging.getLogger(__name__)


class App(AppConfig):
    name = 'theming'

    class Defaults:
        THEMING_DEFAULT_THEME = 'default'
        THEMING_ROOT = 'themes'  # will append to BASE_DIR
        THEMING_URL = 'themes'  # will append to STATIC_URL

    def ready(self):
        self.configure()
        self.patch_settings_staticfiles_dirs()

    def configure(self):
        for name in (name for name in dir(self) if name.upper() == name):
            setattr(settings, name, getattr(self, name))

        for name in (name for name in dir(self.Defaults) if name.upper() == name):
            try:
                getattr(settings, name)
            except AttributeError:
                setattr(settings, name, getattr(self.Defaults, name))

    def patch_settings_staticfiles_dirs(self):
        staticfiles_dirs = []
        for theme_slug in os.listdir(settings.THEMING_ROOT):
            if theme_slug.startswith('~'):
                continue

            real_path = os.path.join(settings.THEMING_ROOT, theme_slug, 'static').replace('\\', '/')
            if os.path.isdir(real_path):
                # here we need its path under static so using THEMING_URL
                key = os.path.join(settings.THEMING_URL, theme_slug).replace('\\', '/')
                row = (key, real_path)
                if os.name == 'nt':  # fix for windows
                    row = [r.replace('/', '\\') for r in row]
                staticfiles_dirs.append(row)
            else:
                logger.debug('theme `%s` not found.' % theme_slug)

        PRE_STATICFILES_DIRS = getattr(settings, 'PRE_STATICFILES_DIRS', None)
        if PRE_STATICFILES_DIRS is None:
            PRE_STATICFILES_DIRS = settings.STATICFILES_DIRS
            # so in concurrent calls the STATICFILES_DIRS not raise
            setattr(settings, 'PRE_STATICFILES_DIRS', PRE_STATICFILES_DIRS)

        settings.STATICFILES_DIRS = tuple(PRE_STATICFILES_DIRS) + tuple(staticfiles_dirs)
