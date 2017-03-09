#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup


setup(name='githublabelscopy',
      version='1.1.0',
      description='A tool to copy labels between repositories using Github API',
      url='http://github.com/fpietka/github-labels-copy',
      author='François Pietka',
      author_email='francois@pietka.fr',
      license='MIT',
      packages=['githublabelscopy'],
      long_description=open('README.rst').read(),
      install_requires=[
          'PyGithub==1.32',
          'docopt==0.6.2'
      ],
      entry_points={
          'console_scripts': [
              'github-labels-copy = githublabelscopy.githublabelscopy:main'
          ],
      },
      classifiers=[
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Environment :: Console',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6'
      ],
      zip_safe=True)
