#!/usr/bin/env python

import re
from setuptools import setup, find_packages


# Try to import pypandoc to convert the readme, otherwise ignore it
try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except ImportError:
    long_description = ""

# Configure the package
setup(
    name="Raspberry Pi Twitter Bot",
    version="0.2.2",
    description="A script for sending tweets from the command line.",
    long_description=long_description,
    author="Alexander Gude",
    author_email="alex.public.account@gmail.com",
    url="https://github.com/agude/raspberry-pi-twitter-bot",
    license="MIT",
    platforms=["any"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            't=rpi_twitter.t:main',
            'caltrain-checker=rpi_twitter.modules.caltrain_checker:main',
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Utilities",
    ],
    keywords=[
        "Twitter",
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=[
        'python-dateutil',
        'pytz',
        'tweepy',
    ],
)
