# -*- coding:utf-8 -*-
'''
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

import os

from django.conf import settings
from django.http.response import HttpResponseRedirect

from .models import thememanager
from django.templatetags.static import static


def redirect_to_theme_fav_icon(request):
    theme = thememanager.get_current_theme()
    url = static(os.path.join(settings.THEMING_URL, theme.slug, '/images/favicon.ico'))
    return HttpResponseRedirect(url)
