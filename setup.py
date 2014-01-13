# -*- coding: utf-8 -*-
#!/usr/bin/env python

import os
import sys

import sqltables

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = sqltables.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-sqltables',
    version=version,
    description="""App which allows displaying resu""",
    long_description=readme + '\n\n' + history,
    author='Patryk Ściborek',
    author_email='patryk@sciborek.com',
    url='https://github.com/scibi/django-sqltables',
    packages=[
        'sqltables',
    ],
    include_package_data=True,
    install_requires=[
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-sqltables',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)