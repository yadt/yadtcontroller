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
    Use the function Configuration.load to read a Configuration from a file.

    example configuration file controller.cfg:

        [broadcaster]
        host = broadcaster.domain.tld
        port = 8081
"""

__author__ = 'Marcel Wolf, Maximilien Riehl, Michael Gruber'

from yadtcommons.configuration import YadtConfigParser, ConfigurationException
from logging import getLogger

SECTION_BROADCASTER = 'broadcaster'

BROADCASTER_HOST_KEY = 'broadcaster-host'
BROADCASTER_PORT_KEY = 'broadcaster-port'
TARGET_KEY = 'target'

logger = getLogger('configuration')


class ControllerConfigLoader (object):
    """
        uses a YadtConfigParser which offers convenience methods.
    """
    DEFAULT_BROADCASTER_HOST = 'localhost'
    DEFAULT_BROADCASTER_PORT = '8081'

    def __init__(self, defaults=None):
        """
            Creates instance of YadtConfigParser which will be used to parse the configuration file.
        """
        if defaults:
            self.DEFAULT_BROADCASTER_HOST = defaults.get('--broadcaster-host')
            self.DEFAULT_BROADCASTER_PORT = defaults.get('--broadcaster-port')
        self._parser = YadtConfigParser()

    def get_broadcaster_host(self):
        """
            @return: the broadcaster host from the configuration file,
                     otherwise DEFAULT_BROADCASTER_HOST.
        """
        return self._parser.get_option(SECTION_BROADCASTER, 'host', self.DEFAULT_BROADCASTER_HOST)

    def get_broadcaster_port(self):
        """
            @return: the broadcaster port from the configuration file as int,
                     otherwise DEFAULT_BROADCASTER_PORT.
        """
        return self._parser.get_option_as_int(SECTION_BROADCASTER, 'port', self.DEFAULT_BROADCASTER_PORT)

    def read_configuration_file(self, filename):
        """
            Reads the given configuration file. Uses the YadtConfigParser.

            @return: configuration dictionary
        """
        return self._parser.read_configuration_file(filename)


def load(filename, defaults=None):
    """
        loads configuration from a file.

        @return: Configuration dictionary containing the data from the file.
    """
    config_loader = ControllerConfigLoader(defaults)

    try:
        config_loader.read_configuration_file(filename)
    except ConfigurationException as exception:
        logger.warn(str(exception))

    configuration = {BROADCASTER_HOST_KEY: config_loader.get_broadcaster_host(),
                     BROADCASTER_PORT_KEY: config_loader.get_broadcaster_port()}

    return configuration
