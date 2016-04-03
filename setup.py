#!/usr/bin/python
# -*- coding: latin-1 -*-

"""Setup script."""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

try:
    import pageviewapi
    version = pageviewapi.__version__
except ImportError:
    version = 'Undefined'


classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Utilities'
]
packages = ['pageviewapi']
requires = ['requests', 'attrdict']

setup(
    name='pageviewapi',
    version=version,
    author='Commonists',
    author_email='ps.huard@gmail.com',
    url='http://github.com/Commonists/pageviewapi',
    description='Wikimedia Pageview API client',
    long_description=open('README.md').read(),
    license='MIT',
    packages=packages,
    install_requires=requires,
    classifiers=classifiers
)
