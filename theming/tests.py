# -*- coding:utf-8 -*-
'''
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

import django
from django.http.response import HttpResponseRedirect
from django.test import TestCase
from django.test.client import RequestFactory

from .middleware import ThemingMiddleware
from .models import ThemeManager
from .template import Loader
from .threadlocals import get_thread_variable
from .views import redirect_to_theme_fav_icon


try:
    from django.template.engine import Engine
except ImportError:
    Engine = None


class Test(TestCase):
    @classmethod
    def setUpClass(cls):
        super(Test, cls).setUpClass()

        cls.mgr = ThemeManager()


    def test_find_themes(self):
        themes = self.mgr.find_themes()
        self.assertIn('default', themes)
        self.assertIn('vecto', themes)


    def test_choices(self):
        choices = self.mgr.get_themes_choice()
        ch_keys = list(ch[0] for ch in choices)
        self.assertIn('default', ch_keys)
        self.assertIn('vecto', ch_keys)


    def test_middleware(self):
        mw = ThemingMiddleware()
        rf = RequestFactory()
        request = rf.get('/')

        mw.process_request(request)
        sitetheme = get_thread_variable('sitetheme')
        self.assertIsNone(sitetheme)


    def test_template(self):
        if django.VERSION >= (1, 8):
            loader = Loader(Engine())
        else:
            loader = Loader()

        res = list(loader.get_template_sources('base.html'))
        self.assertGreaterEqual(len(res), 1)

        cont = loader.load_template_source('base.html')
        self.assertGreaterEqual(len(cont[0]), 10)


    def test_view(self):
        res = redirect_to_theme_fav_icon(None)
        self.assertIsInstance(res, HttpResponseRedirect)
