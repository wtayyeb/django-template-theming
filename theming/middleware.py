# -*- coding:utf-8 -*-
'''
@author: wTayyeb  https://github.com/wtayyeb
@license: MIT
'''

from django.contrib.sites.models import Site, SITE_CACHE

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
        try:
            host = request.get_host()
            if host not in SITE_CACHE:
                site = Site.objects.get(domain__iexact=host)
                SITE_CACHE[host] = site
            site = SITE_CACHE[host]

        except (Site.DoesNotExist, KeyError):
            site = None

        try:
            sitetheme = site.sitetheme
        except (AttributeError):
            sitetheme = None

        set_thread_variable('sitetheme', sitetheme)

