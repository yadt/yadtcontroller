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

Either obtain information from a YADT broadcaster, or have a remote YADT receiver execute a command.

Usage:
yadtcontroller [options] <target> <waiting_timeout> <pending_timeout> [--] <cmd> <args>...
yadtcontroller [options] <target> <waiting_timeout> info
yadtcontroller (-h | --help)
yadtcontroller --version

Options:
-h --help     Show this screen.
--version     Show version.
-b <host> --broadcaster-host=<host>   Override broadcaster host to use for publishing [default: localhost].
-p <port> --broadcaster-port=<port>   Override broadcaster port to use for publishing [default: 8081].
--config-file=<config_file> Load configuration from this file                         [default:\
 /etc/yadtshell/controller.cfg].

"""

__version__ = '${version}'

DEFAULT_CONFIGURATION_FILE = '/etc/yadtshell/controller.cfg'
BROADCASTER_PORT_OPTION = '--broadcaster-port'
BROADCASTER_HOST_OPTION = '--broadcaster-host'
PENDING_TIMEOUT_ARGUMENT = '<pending_timeout>'
WAITING_TIMEOUT_ARGUMENT = '<waiting_timeout>'

from logging import basicConfig, INFO, getLogger
from docopt import docopt, parse_defaults
from configuration import BROADCASTER_HOST_KEY, BROADCASTER_PORT_KEY, TARGET_KEY, load
from yadt_controller.event_handler import EventHandler


def run():
    basicConfig(format='[%(levelname)s] %(message)s')
    config = _determine_configuration()

    getLogger().setLevel(INFO)

    handler = EventHandler(config[BROADCASTER_HOST_KEY], config[BROADCASTER_PORT_KEY], config[TARGET_KEY])

    parsed_options = docopt(__doc__, version=__version__)

    if parsed_options.get('info'):
        waiting_timeout = int(parsed_options.get('%s' % WAITING_TIMEOUT_ARGUMENT))
        handler.initialize_for_info_request(timeout=waiting_timeout)

    if parsed_options.get('<cmd>'):
        waiting_timeout = int(parsed_options[WAITING_TIMEOUT_ARGUMENT])
        pending_timeout = int(parsed_options[('%s' % PENDING_TIMEOUT_ARGUMENT)])
        handler.initialize_for_execution_request(waiting_timeout=waiting_timeout, pending_timeout=pending_timeout)


def _determine_configuration():
    parsed_options = docopt(__doc__, version=__version__)
    defaults = _get_defaults()

    configuration_file_name = parsed_options['--config-file']

    config = load(configuration_file_name, defaults)

    config[TARGET_KEY] = parsed_options['<target>']

    if defaults[BROADCASTER_HOST_OPTION] != parsed_options[('%s' % BROADCASTER_HOST_OPTION)]:
        config[BROADCASTER_HOST_KEY] = parsed_options[BROADCASTER_HOST_OPTION]

    if defaults[BROADCASTER_PORT_OPTION] != parsed_options[('%s' % BROADCASTER_PORT_OPTION)]:
        config[BROADCASTER_PORT_KEY] = parsed_options[BROADCASTER_PORT_OPTION]
    return config


def _get_defaults():
    defaults = {}
    for default in parse_defaults(__doc__):
        if default.name in [BROADCASTER_HOST_OPTION, BROADCASTER_PORT_OPTION]:
            defaults[default.name] = default.value
    return defaults
