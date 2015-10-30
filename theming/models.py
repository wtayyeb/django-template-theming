# -*- coding:utf-8 -*-
'''
@author: Wasim
@license: MIT
'''

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


