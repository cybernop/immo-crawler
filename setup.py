#!/usr/bin/env python
import setuptools

setuptools.setup(
    name='immocrawler',
    version='1.0.2',
    description='Python notifications for Telegram',
    author='Alexander Schulze',
    packages=setuptools.find_packages(),
    install_requires=[
        'PyYAML',
        'requests',
    ]
)
