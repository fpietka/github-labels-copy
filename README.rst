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

* -l, --login : using your Github username, you will be prompted for your password
* -t, --token : provide your Github token

Alternatively you can set an environment variable called ``GITHUB_API_TOKEN``. Without any identification mode specified,
it will automatically fallback on it.

Options
-------

There are 3 non exclusive modes:

* -c, --create : creates labels which don't exist on target repository
* -r, --remove : remove labels on target repository  which don't exists on source repository
* -m, --modify : modify labels which don't have the right color code on target repository

Default is full mode, which execute all those actions.
