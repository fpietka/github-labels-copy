.. image:: https://landscape.io/github/fpietka/github-labels-copy/master/landscape.svg?style=flat
   :target: https://landscape.io/github/fpietka/github-labels-copy/master
   :alt: Code Health
.. image:: https://img.shields.io/pypi/v/githublabelscopy.svg
   :target: https://pypi.python.org/pypi/githublabelscopy
   :alt: Version
.. image:: https://img.shields.io/pypi/pyversions/githublabelscopy.svg
   :target: https://pypi.python.org/pypi/githublabelscopy
   :alt: Python versions supported
.. image:: https://img.shields.io/pypi/l/githublabelscopy.svg
   :target: https://pypi.python.org/pypi/githublabelscopy
   :alt: License

==================
Github Labels Copy
==================

A tool to copy labels between repositories using Github API

Here are the actions done by this tool:

- Add missing labels
- Modify color for existing labels
- Delete labels not availlable in source repository

It can be used with either login/password or API Key.

Installation
------------

You can install it using ``pip``::

 $ pip install githublabelscopy

Usage
-----

To copy labels between two repositories::

 $ github-labels-copy myuser/source-repo myuser/target-repo

There is also two identification modes:

* --login : using your Github username, you will be prompted for your password
* --token : provide your Github token

Alternatively you can set an environment variable called ``GITHUB_API_TOKEN``. Without any identification mode specified,
it will automatically fallback on it.

You can also dump/load labels:

* --load : load labels from a previous dump (yaml file)
* --dump : dump labels into a yaml file

Options
-------

There are 3 non exclusive modes:

* -c : creates labels which don't exist on target repository
* -r : remove labels on target repository  which don't exists on source repository
* -m : modify labels which don't have the right color code on target repository

Default is full mode, which execute all those actions.
