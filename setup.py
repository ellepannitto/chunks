#!/usr/bin/env python3
"""structured-distributional-model setup.py.

This file details modalities for packaging the structured-distributional-model package.
"""

from setuptools import setup

with open('README.md', 'r',) as fh:
    long_description = fh.read()

setup(
    name='chunks',
    description='chunks',
    author='Ludovica Pannitto',
    author_email='ludovica.pannitto@unitn.it',
    long_description=long_description,
    long_description_content_type='text/markdown',
    version='0.1.0',
    license='MIT',
    platforms=['any'],
    packages=['chunks', 'chunks.logging', 'chunks.exceptions',
              'chunks.utils', 'chunks.core'],
    package_data={'tfe': ['logging/*.yml']},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'chunks = chunks.main:main'
        ],
    },
    install_requires=['pyyaml>=4.2b1'],
    zip_safe=False,
)
