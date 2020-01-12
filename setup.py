#!/usr/bin/env python
from distutils.core import setup

setup(name='immocrawler',
      version='0.1',
      description='Python notifications for Telegram',
      author='Alexander Schulze',
      author_email='cibernop@gmail.com',
      packages=[
          'immocrawler',
          'immocrawler.inout',
          'immocrawler.provider',
      ],
      install_requires=[
          'pandas==0.25.1',
          'PyYAML==5.1.2',
          'python-telegram-bot==12.2.0',
          'requests==2.22.0',
      ]
      )
