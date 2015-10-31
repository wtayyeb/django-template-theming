# -*- coding:utf-8 -*-
'''
@author: Wasim
@license: MIT
'''

import json
import os

from django.conf import settings
from django.contrib.sites.models import Site
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Theme(models.Model):
	title		 = models.CharField(max_length=100)
	slug		 = models.CharField(max_length=50)

	def __str__(self):
		return self.title


	class Meta:
		verbose_name		 = _('Theme')
		verbose_name_plural	 = _('Themes')



@python_2_unicode_compatible
class SiteTheme(models.Model):
	site		 = models.ForeignKey(Site)
	theme		 = models.ForeignKey(Theme)

	def __str__(self):
		return '%s - %s' % (self.site, self.theme)


	class Meta:
		verbose_name		 = _('SiteTheme')
		verbose_name_plural	 = _('SiteThemes')



class ThemeManager(object):

	_metadata = 'metadata.json'

	def __init__(self):
		self.theme_root = getattr(settings, 'THEME_ROOT', None)
		self.theme_default = getattr(settings, 'DEFAULT_THEME', 'default')
		self.themes = {}

	def add_theme(self, theme):
		if type(theme) is Theme:
			self.themes.update({theme.slug: theme})

	def get_theme(self, slug):
		try:
			if self.theme_root:
				metadata_path = os.path.join(
					self.theme_root, slug, self._metadata
				)
				with open(metadata_path, 'r') as metadata:
					theme = json.load(metadata)
					return Theme(**theme)
			else:
				raise Exception('THEME_ROOT is not defined')
		except IOError as e:
			raise Exception(e)

	def get_default(self):
		return self.get_theme(self.theme_default)

	def search_themes(self):
		try:
			if self.theme_root:
				for (root, dirs, names) in os.walk(self.theme_root):
					if self._metadata in names:
						root_metadata = os.path.join(root, self._metadata)
						with open(root_metadata, 'r') as metadata:
							theme = json.load(metadata)
							theme_obj = Theme(**theme)
							self.add_theme(theme_obj)
				return self.themes
			else:
				raise Exception('THEME_ROOT is not defined')
		except IOError:
			raise Exception('Metadata is malformed')
