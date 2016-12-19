# -*- coding:utf-8 -*-
"""
Created on Nov 22, 2016

@author: Wasim
"""

from compressor.management.commands.compress import Command as CompressorCommand

from theming.models import SiteTheme
from theming.threadlocals import set_thread_variable


class Command(CompressorCommand):
    help = 'override compress command to let themes get effect'

    def handle(self, *args, **options):
        done = False
        for sitetheme in SiteTheme.objects.all():
            print '# Run compress command for Site:', sitetheme.site
            set_thread_variable('sitetheme', sitetheme)
            super(Command, self).handle(*args, **options)
            done = True

        if done is False:
            print '# cannot find any sitetheme, fall back to pure compress command'
            super(Command, self).handle(*args, **options)
