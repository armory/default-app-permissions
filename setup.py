#!/usr/bin/env python

from setuptools import setup, find_packages
from os.path import join, dirname

setup(name='default_app_permisions',
      description='An simple script that modifies app permissions',
      author='Armory, Inc',
      version='0.0.1',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'requests',
      ],
      entry_points={
          "console_scripts": [
              "default-app-permissions = default_app_permissions.main:main"
          ]
      }
)
