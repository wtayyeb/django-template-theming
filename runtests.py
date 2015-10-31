#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.core.management import execute_from_command_line


# Give feedback on used versions
sys.stderr.write('Using Python version {0} from {1}\n'.format(
    sys.version[:5],
    sys.executable)
)
sys.stderr.write('Using Django version {0} from {1}\n'.format(
    django.get_version(),
    os.path.dirname(os.path.abspath(django.__file__)))
)

if not settings.configured:
    settings.configure(
        DEBUG=True,
        TEMPLATE_DEBUG=True,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': ':memory:'
            }
        },
        TEMPLATE_LOADERS=(
            'django.template.loaders.app_directories.Loader',
        ),
#         TEMPLATE_CONTEXT_PROCESSORS=tuple(default_settings.TEMPLATE_CONTEXT_PROCESSORS) + (
#             'django.core.context_processors.request',
#         ),
        TEST_RUNNER='django.test.runner.DiscoverRunner' if django.VERSION >= (1, 7) else 'django.test.simple.DjangoTestSuiteRunner',
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.messages',
            'django.contrib.sites',
            'django.contrib.admin',

            'theming',
        ),
        MIDDLEWARE_CLASSES=(
            'theming.middleware.ThemingMiddleware',
        ),
        SITE_ID=2,

        THEMING_ROOT=os.path.join(os.path.dirname(__file__), 'example', 'themes')
    )


def runtests():
    argv = sys.argv[:1] + ['test', 'theming', '--traceback'] + sys.argv[1:]
    execute_from_command_line(argv)

if __name__ == '__main__':
    runtests()
