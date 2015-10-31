# -*- coding:utf-8 -*-
'''
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

from .models import ThemeManager
from .threadlocals import set_thread_variable


class ThemingMiddleware(object):
    ''' Middleware that puts the request object in thread local storage.

        add this middleware to MIDDLEWARE_CLASSES to make theming work.

        MIDDLEWARE_CLASSES	 = (
            ...
            'theming.middleware.ThemingMiddleware',
        )

    '''

    def process_request(self, request):
        host = request.get_host()
        mgr = ThemeManager()
        mgr.set_host(host)
        
        # why ?
        set_thread_variable('theme_manager', mgr)

        # why ?
        set_thread_variable('request', request)
