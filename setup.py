#!/usr/bin/env python
import setuptools

setuptools.setup(
    name='immocrawler',
    version='0.1',
    description='Python notifications for Telegram',
    author='Alexander Schulze',
    author_email='cibernop@gmail.com',
    packages=setuptools.find_packages(),
    install_requires=[
        'PyYAML',
        'requests',
    ]
)
