#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of home-mqtt-url-relay.
# https://github.com/garaemon/home-mqtt-url-relay

# Licensed under the MIT license:
# http://www.opensource.org/licenses/MIT-license
# Copyright (c) 2017, garaemon <garaemon@gmail.com>

from setuptools import setup, find_packages
from home_mqtt_url_relay import __version__

tests_require = [
    'mock',
    'nose',
    'coverage',
    'yanc',
    'preggy',
    'tox',
    'ipdb',
    'coveralls',
    'sphinx',
]

setup(
    name='home-mqtt-url-relay',
    version=__version__,
    description='an incredible python package',
    long_description='''
an incredible python package
''',
    keywords='',
    author='garaemon',
    author_email='garaemon@gmail.com',
    url='https://github.com/garaemon/home-mqtt-url-relay',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.4',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    include_package_data=False,
    install_requires=[
       'fire', 'paho-mqtt',
    ],
    extras_require={
        'tests': tests_require,
    },
    entry_points={
        'console_scripts': [
            # add cli scripts here in this form:
            'home-mqtt-url-relay=home_mqtt_url_relay.cli:main',
            'home-mqtt-url-relay-deploy=home_mqtt_url_relay.deploy:main',
        ],
    },
)
