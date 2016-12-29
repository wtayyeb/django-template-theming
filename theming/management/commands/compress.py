# -*- coding:utf-8 -*-
"""
Created on Nov 22, 2016

@author: Wasim
"""

from optparse import make_option
from urlparse import urlparse

from compressor.management.commands.compress import Command as CompressorCommand
from django.contrib.auth.models import User
from django.test.client import RequestFactory

from theming.middleware import ThemingMiddleware
from theming.models import SiteTheme
from theming.threadlocals import set_thread_variable, get_thread_variable


class Command(CompressorCommand):
    help = 'override compress command to let themes get effect'

    option_list = CompressorCommand.option_list + (
        make_option('--base-url', '-b', action='store', dest='base_url', default=None,
            help='just compress for given base_url'),
    )

    def handle(self, *args, **options):
        base_url = options.get('base_url')

        if base_url is None:
            all_sitethemes = SiteTheme.objects.all()

        else:
            factory = RequestFactory()
            self.request = request = factory.request()
            request.META['SERVER_NAME'] = urlparse(base_url).netloc
            request.user = User(is_superuser=False)
            try:
                from aliassite.middleware import AliasSiteMiddleware
                AliasSiteMiddleware().process_request(request)
            except ImportError:
                pass

            ThemingMiddleware().process_request(request)
            sitetheme = get_thread_variable('sitetheme')
            all_sitethemes = [sitetheme, ]


        for sitetheme in all_sitethemes:
            if sitetheme is None:
                print('# cannot find any sitetheme, fall back to pure compress command')
            else:
                print('# Run compress command for Site:%s Theme:%s' % (sitetheme.site, sitetheme.theme))
            set_thread_variable('sitetheme', sitetheme)
            super(Command, self).handle(*args, **options)
