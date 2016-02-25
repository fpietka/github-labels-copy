#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='githublabelscopy',
      version='1.0.0',
      description='A tool to copy labels between repositories using Github API',
      url='http://github.com/fpietka/github-labels-copy',
      author='François Pietka',
      author_email='francois[at]]pietka[dot]fr',
      license='MIT',
      packages=find_packages(),
      long_description=open('README.rst').read(),
      install_requires=[
          'PyGithub==1.25.2'
      ],
      entry_points={
          'console_scripts': [
              'github-labels-copy = githublabelscopy.githublabelscopy:main'
          ],
      },
      classifiers=[
          'Intended Audience :: Developers',
          'Environment :: Console',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4'
      ],
      zip_safe=True)
