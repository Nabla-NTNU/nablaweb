#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from setuptools import setup, find_packages

from content import VERSION

requirements = [
    'markdown',
    'pytz',
    'django-haystack',
    'django>=1.8',
    'django-contrib-comments',
    'django-image-cropping',
    'django-filebrowser',
    'Pillow',
    'easy-thumbnails',
    'django-braces',
    'django-sekizai>=0.8.2',
    'django-markdown-deux',
    'django-nyt>=1.0b1'
]

setup(
    name="content",
    version=VERSION,
    author="Webkom",
    description="A common functionality app for django.",
    keywords="django content",
    packages=find_packages(exclude=["testproject", "testproject.*"]),
    zip_safe=False,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    include_package_data=True,
)
