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

"""
yadtcontroller

Usage:
yadtcontroller (-h | --help)
yadtcontroller --version
yadtcontroller [--broadcaster-host=<host>] [--broadcaster-port=<port>] [--config-file=<config_file]

Options:
-h --help     Show this screen.
--version     Show version.
--broadcaster-host=<host>
--broadcaster-port=<port>
--config-file=<config_file>

"""

__version__ = '${version}'

from docopt import docopt

from configuration import BROADCASTER_HOST_KEY, BROADCASTER_PORT_KEY, load
from yadt_controller.request_emitter import RequestEmitter


def run():
    config = _determine_configuration()

    RequestEmitter(config[BROADCASTER_HOST_KEY], config[BROADCASTER_PORT_KEY])


def _determine_configuration():
    parsed_options = docopt(__doc__, version=__version__)
    configuration_file_name = '/etc/yadtshell/controller.cfg'
    if parsed_options.get('--config-file') is not None:
        configuration_file_name = parsed_options['--config-file']
    config = load(configuration_file_name)
    if parsed_options.get('--broadcaster-host') is not None:
        config[BROADCASTER_HOST_KEY] = parsed_options['--broadcaster-host']
    if parsed_options.get('--broadcaster-port') is not None:
        config[BROADCASTER_PORT_KEY] = parsed_options['--broadcaster-port']
    return config
