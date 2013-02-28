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
yadtcontroller <target> [--broadcaster-host=<host> --broadcaster-port=<port> --config-file=<config_file>]
yadtcontroller (-h | --help)
yadtcontroller --version

Options:
-h --help     Show this screen.
--version     Show version.
--broadcaster-host=<host>   Override broadcaster host to use for publishing [default: localhost].
--broadcaster-port=<port>   Override broadcaster port to use for publishing [default: 8081].
--config-file=<config_file> Load configuration from this file               [default: /etc/yadtshell/controller.cfg].

"""

__version__ = '${version}'

DEFAULT_CONFIGURATION_FILE = '/etc/yadtshell/controller.cfg'

from logging import basicConfig, INFO, getLogger
from docopt import docopt
from configuration import BROADCASTER_HOST_KEY, BROADCASTER_PORT_KEY, TARGET_KEY, load
from yadt_controller.event_handler import EventHandler


def run():
    basicConfig(format='[%(levelname)s] %(message)s')
    config = _determine_configuration()

    getLogger().setLevel(INFO)

    request_emitter = EventHandler(config[BROADCASTER_HOST_KEY], config[BROADCASTER_PORT_KEY], config[TARGET_KEY])
    request_emitter.initialize()


def _determine_configuration():
    parsed_options = docopt(__doc__, version=__version__)
    configuration_file_name = parsed_options['--config-file']

    config = load(configuration_file_name)
    config[TARGET_KEY] = parsed_options['<target>']

    config[BROADCASTER_HOST_KEY] = parsed_options['--broadcaster-host']

    config[BROADCASTER_PORT_KEY] = parsed_options['--broadcaster-port']

    return config
