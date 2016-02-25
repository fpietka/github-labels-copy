#!/usr/bin/env python

"""
Github Label Copy

This allow you to copy and/or update labels from a source repository
to another.
"""

from sys import exit
from os import getenv
from .__init__ import __version__
import argparse
from .labels import Labels

# to catch connection error
import socket
import github
from github.GithubException import UnknownObjectException, TwoFactorException, \
    BadCredentialsException

parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)

parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))

# Mandatory arguments
parser.add_argument('src_repo', metavar='src_repo', type=str,
                    help='source repository')
parser.add_argument('dst_repo', metavar='dst_repo', type=str,
                    help='destination repository')

# Optional arguments
group = parser.add_mutually_exclusive_group()
group.add_argument('-t', '--token', metavar='token', type=str, nargs='?',
                   help='a token to identify on Github')
group.add_argument('-l', '--login', metavar='login', type=str, nargs='?',
                   help='a login to identify on Github')

# Copy modes
mode = parser.add_argument_group()
# default = full (like -crm)
mode.add_argument('-c', '--create', action='store_true',
                  help='create new labels')
mode.add_argument('-r', '--remove', action='store_true',
                  help='remove old labels')
mode.add_argument('-m', '--modify', action='store_true',
                  help='modify changed labels')


class NoCredentialException(Exception):
    pass


def main():
    args = parser.parse_args()
    if args.login:
        labels = Labels(login=args.login)
    elif args.token:
        labels = Labels(token=args.token)
    else:
        token = getenv('GITHUB_API_TOKEN')
        if token:
            labels = Labels(token=token)
        else:
            raise NoCredentialException()

    labels.setSrcRepo(args.src_repo)
    labels.setDstRepo(args.dst_repo)

    if args.create:
        labels.createMissing()
    if args.remove:
        labels.deleteBad()
    if args.modify:
        labels.updateWrong()
    if not args.create and not args.remove and not args.modify:
        labels.fullCopy()


if __name__ == '__main__':
    try:
        main()
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
