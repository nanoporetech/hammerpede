#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from glob import glob

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='Hammerpede',
    version='0.1.0',
    description="Hammerpede.",
    long_description=readme,
    author="ONT Applications Group",
    author_email='Apps@nanoporetech.com',
    url='',
    packages=[
        'hammerpede',
    ],
    package_dir={'hammerpede':
                 'hammerpede'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    keywords='hammerpede',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 3",
    ],
    tests_require=test_requirements,
    scripts=[x for x in glob('scripts/*.py') if x != 'scripts/__init__.py']
)
