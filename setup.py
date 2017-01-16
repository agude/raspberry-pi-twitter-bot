#!/usr/bin/env python3

import re
from setuptools import setup, find_packages


# Get the version from the main script
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open("rpi_twitter/t.py").read(),
    re.M
).group(1)

# Try to import pypandoc to convert the readme, otherwise ignore it
#try:
#    import pypandoc
#    long_description = pypandoc.convert('README.md', 'rst')
#except ImportError:
#    long_description = ""

# Configure the package
setup(
    name="Raspberry Pi Twitter Bot",
    version=version,
    description="A script for sending tweets from the command line.",
    #long_description=long_description,
    author="Alexander Gude",
    author_email="alex.public.account@gmail.com",
    url="https://github.com/agude/raspberry-pi-twitter-bot",
    license="MIT",
    platforms=["any"],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            't=rpi_twitter.t:main'
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
    install_requires=['tweepy'],
)
