#!/usr/bin/env python
from __future__ import absolute_import
from __future__ import unicode_literals

from setuptools import setup, find_packages

requirements = [
    'django>=1.8',
    'django-image-cropping',
    'django-sekizai>=0.8.2',
    'easy-thumbnails',
    'markdown',
]

setup(
    name="content",
    version="0.3",
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
