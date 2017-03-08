#!/usr/bin/env python

"""Github Label Copy

This allow you to copy and/or update labels from a source repository
to another.

Usage:
  github-labels-copy [--login=<login> | --token=<token>] [-crm]
                     SOURCE DESTINATION
  github-labels-copy (-h | --help)
  github-labels-copy --version

Arguments:
  SOURCE        Source repository (e.g. user/repository)
  DESTINATION   Destination repository (e.g. user/repository)

Options:
  -h --help         Show this screen.
  --version         Show version.
  --token=TOKEN     Github access token.
  --login=LOGIN     Github login, you will be prompted for password.
  -c                Create labels that are in source but not in destination
                    repository.
  -r                Remove labels that are in destination but not in source
                    repository.
  -m                Modify labels existing in both repositories but with a
                    different color.

"""

from os import getenv
from docopt import docopt
from .labels import Labels

# to catch connection error
import socket
from github.GithubException import (UnknownObjectException, TwoFactorException,
                                    BadCredentialsException)

__version__ = '1.0.0'


class NoCredentialException(Exception):
    pass


def label_copy():
    args = docopt(__doc__)
    if args['--login']:
        labels = Labels(login=args['--login'])
    elif args['--token']:
        labels = Labels(token=args['--token'])
    else:
        token = getenv('GITHUB_API_TOKEN')
        if token:
            labels = Labels(token=token)
        else:
            raise NoCredentialException()

    labels.setSrcRepo(args['SOURCE'])
    labels.setDstRepo(args['DESTINATION'])

    if args['-c']:
        labels.createMissing()
    if args['-r']:
        labels.deleteBad()
    if args['-m']:
        labels.updateWrong()
    if not args['-c'] and not args['-r'] and not args['-m']:
        labels.fullCopy()


def main():
    try:
        label_copy()
    except socket.error as e:
        raise Exception('Connection error', e)
    except UnknownObjectException:
        raise Exception("Repository not found. Check your credentials.")
    except TwoFactorException:
        raise Exception("Two factor authentication required.")
    except BadCredentialsException:
        raise Exception("Bad credentials")
    except NoCredentialException:
        raise Exception("Missing credentials")


if __name__ == '__main__':
    main()
