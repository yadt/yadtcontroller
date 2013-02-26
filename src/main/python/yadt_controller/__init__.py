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
yadtcontroller [--broadcaster_host=<broadcaster_host>] [--broadcaster_port=<broadcaster_port>] [--config-file=<config_file]

Options:
-h --help     Show this screen.
--version     Show version.
--broadcaster_host=<broadcaster_host>
--broadcaster_port=<broadcaster_port>
--config-file=<config_file>

"""

__version__ = '${version}'

from docopt import docopt

import configuration
from yadt_controller.request_emitter import RequestEmitter


def run():
    parsed_options = docopt(__doc__, version=__version__)

    configuration_file_name = '/etc/yadtshell/controller.cfg'
    if '--config-file' in parsed_options and parsed_options['--config-file'] is not None:
        configuration_file_name = parsed_options['--config-file']
    config = configuration.load(configuration_file_name)

    RequestEmitter(config['broadcaster_host'], config['broadcaster_port'])
