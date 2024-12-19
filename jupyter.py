#!/usr/bin/env python3.9

''' jupyter: launch and manage Jupyter HPC jobs '''

###############################################################################
#     __  _  _  ____  _  _  ____  ____  ____
#   _(  )/ )( \(  _ \( \/ )(_  _)(  __)(  _ \
#  / \) \) \/ ( ) __/ )  /   )(   ) _)  )   /
#  \____/\____/(__)  (__/   (__) (____)(__\_)
#
###############################################################################


import argparse
from random import choices
from string import hexdigits
import sys

from rich import print
from rich_argparse import RawDescriptionRichHelpFormatter

from jupyter_manager import \
    __prog__, __version__, __status__, SESSION_STORE, R_VERSIONS
from jupyter_manager.commands import jupyter_start, jupyter_stop, jupyter_list


# argparse ####################################################################


commands = {}

parser = argparse.ArgumentParser(
    prog='__prog__',
    description=r'''
                   __  _  _  ____  _  _  ____  ____  ____
                 _(  )/ )( \(  _ \( \/ )(_  _)(  __)(  _ \
                / \) \) \/ ( ) __/ )  /   )(   ) _)  )   /
                \____/\____/(__)  (__/   (__) (____)(__\_)

                    launch and manage Jupyter HPC jobs
''',
    formatter_class=RawDescriptionRichHelpFormatter,
    exit_on_error=False,
    allow_abbrev=False)
subparsers = parser.add_subparsers(
    title='commands',
    metavar='{command}',
    dest='command',
    required=True)

parser.add_argument(
    '-v', '--version',
    action='version', version=f'{__prog__} v{__version__} ({__status__})',
    help='show the program version and exit')
parser.add_argument(
    '-q', '--quiet', action='store_true',
    help='silence logging information')

#
# jupyter start
#

commands['start'] = subparsers.add_parser(
    'start',
    aliases=['create', 'new'],
    help='start a new Jupyter server',
    description='start a new Jupyter server',
    formatter_class=RawDescriptionRichHelpFormatter)
# register the alias names as placeholders
commands['create'] = commands['new'] = commands['start']
# arguments
commands['start'].add_argument(
    'r_version', choices=R_VERSIONS,
    help='version of Python to launch as the default Jupyter kernel')
commands['start'].add_argument(
    '-n', '--name', default='jupyter_server', type=str,
    help='job name for the scheduler (default "%(default)s")')
commands['start'].add_argument(
    '-@', '--cpu', default=1, type=int,
    help='requested number of CPUs (default %(default)s)')
commands['start'].add_argument(
    '-m', '--mem', default=8, type=int,
    help='requested amount of RAM (GB, default %(default)s)')
commands['start'].add_argument(
    '-w', '--wallclock', dest='time', default=16, type=int,
    help='requested runtime (hrs, default %(default)s)')
commands['start'].add_argument(
    '-g', '--gpu', default=0, type=int,
    help='requested number of GPUs (default %(default)s)')
commands['start'].add_argument(  # hidden
    '-p', '--partition', default='int', type=str,
    choices=('int', 'cpu', 'hmem', 'gpu'),
    help=argparse.SUPPRESS)
commands['start'].add_argument(
    '-b', '--bind', type=str, default='',
    help='additional bind path/s using the singularity format \
    specification (src[:dest[:opts]])')
commands['start'].add_argument(  # hidden
    '-l', '--log', action='store_true',
    help=argparse.SUPPRESS)

#
# jupyter stop
#

commands['stop'] = subparsers.add_parser(
    'stop',
    aliases=['delete', 'cancel', 'kill'],
    help='stop an existing Jupyter server instance',
    description='stop an existing Jupyter server instance',
    formatter_class=RawDescriptionRichHelpFormatter)
# register the alias names as placeholders
commands['delete'] = commands['cancel'] = commands['kill'] = commands['stop']
# arguments
commands['stop'].add_argument(
    'job', type=str, nargs='*',
    help='list of job number/s and/or name/s to kill')
commands['stop'].add_argument(
    '-a', '--all', action='store_true',
    help='stop all running Jupyter instances')

#
# jupyter list
#

commands['list'] = subparsers.add_parser(
    'list',
    aliases=['ls', 'show'],
    help='list running Jupyter servers',
    description='list running Jupyter servers',
    formatter_class=RawDescriptionRichHelpFormatter)
# register the alias names as placeholders
commands['ls'] = commands['show'] = commands['list']


# main ########################################################################


def main():

    # catch program name by itself
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    # catch command names by themselves
    if len(sys.argv) == 2 and \
            (sys.argv[1] in commands and
            sys.argv[1] not in ('list', 'ls', 'show')):
        commands[sys.argv[1]].print_help()
        sys.exit(0)

    # catch unknown commands and errors
    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help()
        sys.exit(1)

    # Run the relevant command from jupyter_manager.commands
    if args.command in ('start', 'create'):
        jupyter_start(args)
    elif args.command in ('stop', 'delete', 'cancel', 'kill'):
        jupyter_stop(args)
    elif args.command in ('list', 'ls', 'show'):
        jupyter_list(args)


if __name__ == '__main__':
    main()
