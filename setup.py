
from codecs import open
from os import path

from setuptools import setup, find_packages

import theming


BASE = path.abspath(path.dirname(__file__))

with open(path.join(BASE, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-template-theming',
    version=theming.__version__,
    url='https://github.com/wtayyeb/django-template-theming',
    author='w.Tayyeb',
    author_email='tayyeb@tsaze.com',

    description=('Django application, implement theming concept, '
                 'flexible and configurable.'),
    license='MIT',

    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    install_requires=[
        'django-appconf',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    keywords='django template theme theming host',
)
