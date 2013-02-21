#   yadtcontroller
#   Copyright (C) 2013 Immobilien Scout GmbH
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

__version__ = '${version}'

from sys import stdout
from docopt import docopt

__usage__ = \
"""yadtcontroller.

Usage:
yadtcontroller (-h | --help)    
yadtcontroller --version

Options:
-h --help     Show this screen.
--version     Show version.

"""


def run():
    parsed_arguments = docopt(__usage__, version=__version__)
    if _show_version_option_was_given(parsed_arguments):
        print_name_and_version_and_exit()


def write(text):
    stdout.write(text)


def print_name_and_version_and_exit():
    write('yadtcontroller {0}'.format(__version__))


def _show_version_option_was_given(parsed_arguments):
    return parsed_arguments and parsed_arguments['--version']