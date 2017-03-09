#!/usr/bin/env python

"""Github Label Copy

This allow you to copy and/or update labels from a source repository
to another.

Usage:
  github-labels-copy [--login=<login> | --token=<token>] [-crm]
                     (--load=<file> | SOURCE) (--dump | DESTINATION)
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
  --load=FILE       Load labels from a previous dump.
  --dump            Dump labels into a yaml file.
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

__version__ = '1.1.0'

dump_file = 'labels.yaml'


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

    if args['--load']:
        labels.load(args['--load'])
    else:
        labels.setSrcRepo(args['SOURCE'])

    if args['--dump']:
        labels.activateDumpMode()
    else:
        labels.setDstRepo(args['DESTINATION'])

    if args['-c']:
        labels.createMissing()
    if args['-r']:
        labels.deleteBad()
    if args['-m']:
        labels.updateWrong()
    if not args['-c'] and not args['-r'] and not args['-m']:
        labels.fullCopy()

    if args['--dump']:
        print('Dumping labels into {}'.format(dump_file))
        with open(dump_file, 'w+') as fh:
            fh.write(labels.dump())


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
