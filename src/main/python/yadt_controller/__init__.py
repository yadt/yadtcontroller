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

The yadtcontroller application is connects to a YADT broadcaster and
issue orders to connected YADT receivers through the broadcaster, or retrieves
information from the broadcaster directly.

Usage:
yadtcontroller [options] <target> <waiting_timeout> <pending_timeout> [--] <cmd> <args>...
yadtcontroller [options] <target> <waiting_timeout> info
yadtcontroller (-h | --help)
yadtcontroller --version

Options:
-h --help     Show this screen.
--version     Show version.
-v --verbose  Spit out a lot of information.
-q --quiet    Be especially quiet (overrides the verbose flag).
--teamcity    Use TeamCity progress messages.
--broadcaster-host=<host>   Override broadcaster host to use for publishing [default: localhost].
--broadcaster-port=<port>   Override broadcaster port to use for publishing [default: 8081].
--config-file=<config_file> Load configuration from this file               [default: /etc/yadtshell/controller.cfg].

"""

__version__ = '${version}'

DEFAULT_CONFIGURATION_FILE = '/etc/yadtshell/controller.cfg'
CONFIG_FILE_OPTION = '--config-file'
BROADCASTER_PORT_OPTION = '--broadcaster-port'
BROADCASTER_HOST_OPTION = '--broadcaster-host'
PENDING_TIMEOUT_ARGUMENT = '<pending_timeout>'
WAITING_TIMEOUT_ARGUMENT = '<waiting_timeout>'
TARGET_ARGUMENT = '<target>'
COMMAND_ARGUMENT = '<cmd>'
ARGUMENT_ARGUMENT = '<args>'
INFO_COMMAND = 'info'

MINIMAL_WAITING_TIMEOUT = 30


from logging import basicConfig, INFO, DEBUG, WARN, getLogger

from docopt import docopt, parse_defaults

from configuration import BROADCASTER_HOST_KEY, BROADCASTER_PORT_KEY, TARGET_KEY, load
from yadt_controller.event_handler import EventHandler
from yadt_controller.tracking import generate_tracking_id
from yadt_controller.terminal import TeamCityProgressMessageHandler


def run():
    basicConfig(format='%(asctime)s [%(levelname)7s] %(message)s')
    getLogger().setLevel(INFO)

    parsed_options = docopt(__doc__, version=__version__)

    _apply_log_level_configuration_from_options(parsed_options)

    config = _determine_configuration()

    event_handler = EventHandler(
        config[BROADCASTER_HOST_KEY], config[BROADCASTER_PORT_KEY], config[TARGET_KEY])

    progress_handler = None
    if parsed_options.get('--teamcity'):
        progress_handler = TeamCityProgressMessageHandler()

    logger = getLogger('yadt_controller')

    if parsed_options.get(INFO_COMMAND):
        waiting_timeout = int(parsed_options.get(WAITING_TIMEOUT_ARGUMENT))
        info_command_debug_message = 'Requesting info on target {0}. Will wait at most {1} second(s) for a reply.'
        logger.debug(info_command_debug_message.format(
            event_handler.target, waiting_timeout))
        event_handler.initialize_for_info_request(timeout=waiting_timeout)

    if parsed_options.get(COMMAND_ARGUMENT):
        waiting_timeout = int(parsed_options[WAITING_TIMEOUT_ARGUMENT])
        if waiting_timeout < MINIMAL_WAITING_TIMEOUT:
            message = ('Given waiting timeout (%rs) is less than minimal allowed timeout (%rs), ' +
                       'using the minimal timeout instead.')
            logger.warning(
                message % (waiting_timeout,
                           MINIMAL_WAITING_TIMEOUT))
            waiting_timeout = MINIMAL_WAITING_TIMEOUT
        pending_timeout = int(parsed_options[PENDING_TIMEOUT_ARGUMENT])
        command_to_execute = parsed_options[COMMAND_ARGUMENT]
        arguments = parsed_options[ARGUMENT_ARGUMENT]

        tracking_id = _add_generated_tracking_id_to_arguments(
            arguments, event_handler)

        message = ('Requesting execution of {0} with arguments {1} on target {2}. Will wait {3} seconds for the ' +
                   'command to start, and {4} seconds for the command to complete.')
        logger.debug(message.format(command_to_execute,
                                    arguments,
                                    event_handler.target,
                                    waiting_timeout,
                                    pending_timeout))

        event_handler.initialize_for_execution_request(
            waiting_timeout=waiting_timeout,
            pending_timeout=pending_timeout,
            command_to_execute=command_to_execute,
            arguments=arguments,
            tracking_id=tracking_id,
            progress_handler=progress_handler)


def _determine_configuration():
    parsed_options = docopt(__doc__, version=__version__)
    defaults = _get_defaults()

    configuration_file_name = parsed_options[CONFIG_FILE_OPTION]

    config = load(configuration_file_name, defaults)

    config[TARGET_KEY] = parsed_options[TARGET_ARGUMENT]

    if defaults[BROADCASTER_HOST_OPTION] != parsed_options[BROADCASTER_HOST_OPTION]:
        config[BROADCASTER_HOST_KEY] = parsed_options[BROADCASTER_HOST_OPTION]

    if defaults[BROADCASTER_PORT_OPTION] != parsed_options[BROADCASTER_PORT_OPTION]:
        config[BROADCASTER_PORT_KEY] = parsed_options[BROADCASTER_PORT_OPTION]
    return config


def _get_defaults():
    defaults = {}
    for default in parse_defaults(__doc__):
        if default.name in [BROADCASTER_HOST_OPTION, BROADCASTER_PORT_OPTION]:
            defaults[default.name] = default.value
    return defaults


def _apply_log_level_configuration_from_options(parsed_options):
    if parsed_options.get('--verbose'):
        getLogger().setLevel(DEBUG)
    if parsed_options.get('--quiet'):
        getLogger().setLevel(WARN)


def _add_generated_tracking_id_to_arguments(arguments, handler):
    tracking_id = generate_tracking_id(handler.target)
    arguments.append('--tracking-id={0}'.format(tracking_id))
    return tracking_id
