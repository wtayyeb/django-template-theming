# -*- coding:utf-8 -*-
'''
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

import json
import logging
import os

from django.conf import settings
from django.contrib.sites.models import Site, SITE_CACHE
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _  # @UnusedImport

from . import confs  # to set default confs  @UnusedImport - do not remove
from .threadlocals import get_thread_variable


logger = logging.getLogger(__name__)



@python_2_unicode_compatible
class Theme(object):
    _metadata_filename = 'metadata.json'

    def __init__(self, slug, *args, **kwargs):
        super(Theme, self).__init__(*args, **kwargs)

        self.slug = slug
        self._metadata = {}
        self.metadata_ready = None


    def read_metadata(self):
        filename = os.path.join(settings.THEMING_ROOT, self.slug, self._metadata_filename)
        try:
            with open(filename, 'r') as f:
                self._metadata = json.load(f)
                self.metadata_ready = True
        except IOError:
            self._metadata = {}
            self.metadata_ready = False


    def __getattr__(self, key):
        if key not in ('name', 'description', 'author', 'version'):
            raise AttributeError

        if self.metadata_ready is None:
            self.read_metadata()

        if self.metadata_ready is False:
            logger.debug('theme %s have no metadata or its metadata is not a valid json' % self.slug)

        val = self._metadata.get(key)

        if val is None and key is 'name':
            val = self.slug.title()

        return val


    def __str__(self, *args, **kwargs):
        return '<Theme `%s`>' % self.slug



class ThemeManager(object):
    def __init__(self, *args, **kwargs):
        super(ThemeManager, self).__init__(*args, **kwargs)

        self._themes = None
        self.host = None

        self.patch_settings_staticfiles_dirs()


    def find_themes(self, force=False):
        if self._themes is None or force:
            self._themes = {}
            root = settings.THEMING_ROOT
            for dirname in os.listdir(root):
                if not dirname.startswith('~'):
                    self._themes[dirname] = Theme(dirname)

        return self._themes


    def get_themes_choice(self):
        themes = self.find_themes()
        choices = []
        for theme in themes.values():
            choices.append((theme.slug, theme.name))
        return choices


    def get_current_theme(self):
        sitetheme = get_thread_variable('sitetheme')
        if sitetheme:
            theme = sitetheme.theme
        else:
            theme = self.get_theme(settings.THEMING_DEFAULT_THEME)
        return theme


    def get_theme(self, theme_slug):
        self.find_themes()
        return self._themes[theme_slug]


    def patch_settings_staticfiles_dirs(self):
        staticfiles_dirs = []
        for theme_slug in self.find_themes():
            real_path = os.path.join(settings.THEMING_ROOT, '%s/static' % theme_slug)
            if os.path.isdir(real_path):
                key = os.path.join(settings.THEMING_URL, theme_slug)
                staticfiles_dirs.append((key, real_path))
                if os.name == 'nt':     # hack for windows
                    staticfiles_dirs.append((key.replace('/', '\\'), real_path))
            else:
                logger.debug('theme `%s` not found.' % theme_slug)

        PRE_STATICFILES_DIRS = getattr(settings, 'PRE_STATICFILES_DIRS', None)
        if PRE_STATICFILES_DIRS is None:
            PRE_STATICFILES_DIRS = settings.STATICFILES_DIRS
            setattr(settings, 'PRE_STATICFILES_DIRS', PRE_STATICFILES_DIRS)

        settings.STATICFILES_DIRS = tuple(PRE_STATICFILES_DIRS) + tuple(staticfiles_dirs)


thememanager = ThemeManager()



@python_2_unicode_compatible
class SiteTheme(models.Model):
    site = models.OneToOneField(Site)
    theme_slug = models.CharField(max_length=100, choices=thememanager.get_themes_choice())


    @property
    def theme(self):
        return thememanager.get_theme(self.theme_slug)


    def __str__(self):
        theme = self.theme
        return '%s : [%s] %s' % (self.site, theme.slug, theme.name)


    def delete(self, using=None):
        SITE_CACHE.pop(self.site.domain, None)
        return super(SiteTheme, self).delete(using=using)


    def save(self, *args, **kwargs):
        SITE_CACHE.pop(self.site.domain, None)
        return super(SiteTheme, self).save(*args, **kwargs)


