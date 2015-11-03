# -*- coding:utf-8 -*-
'''
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

import os

from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.templatetags.static import static

from .models import thememanager


def redirect_to_theme_fav_icon(request):
    theme = thememanager.get_current_theme()
    favicon = os.path.join(settings.THEMING_URL, theme.slug, 'images/favicon.ico').replace('\\', '/')
    url = static(favicon)
    return HttpResponseRedirect(url)
