# -*- coding:utf-8 -*-
'''
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

from django.test import TestCase

from .models import ThemeManager


class Test(TestCase):
    def test_find_themes(self):
        mgr = ThemeManager()
        print mgr.find_themes()
        print mgr.get_themes_choice()
