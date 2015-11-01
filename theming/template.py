# -*- coding:utf-8 -*-
'''
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

import io

from django.conf import settings
from django.template import TemplateDoesNotExist
from django.utils._os import safe_join

from .models import thememanager


try:
    from django.core.exceptions import SuspiciousFileOperation
except ImportError:
    from django.core.exceptions import SuspiciousOperation as SuspiciousFileOperation

try:
    from django.template.loaders.base import Loader as BaseLoader
except ImportError:
    from django.template.loader import BaseLoader



class Loader(BaseLoader):
    is_usable = True

    def get_template_sources(self, template_name, template_dirs=None):
        """
        Returns the absolute paths to "template_name", when appended to each
        directory in "template_dirs". Any paths that don't lie inside one of the
        template dirs are excluded from the result set, for security reasons.
        """
        theme = thememanager.get_current_theme()

        if not template_dirs:
            template_dirs = [settings.THEMING_ROOT, ]

        for template_dir in template_dirs:
            try:
                yield safe_join(template_dir, theme.slug, template_name)
            except UnicodeDecodeError:
                # The template dir name was a bytestring that wasn't valid UTF-8.
                raise
            except SuspiciousFileOperation:
                # The joined path was located outside of this particular
                # template_dir (it might be inside another one, so this isn't
                # fatal).
                pass


    def load_template_source(self, template_name, template_dirs=None):
        tried = []
        for filepath in self.get_template_sources(template_name, template_dirs):
            try:
                encoding = self.engine.file_charset if hasattr(self, 'engine') and self.engine else 'utf-8'
                with io.open(filepath, encoding=encoding) as fp:
                    return fp.read(), filepath
            except IOError:
                tried.append(filepath)
        if tried:
            error_msg = "Tried %s" % tried
        else:
            error_msg = "Your TEMPLATE_DIRS setting is empty. Change it to point to at least one template directory."
        raise TemplateDoesNotExist(error_msg)
    load_template_source.is_usable = True


