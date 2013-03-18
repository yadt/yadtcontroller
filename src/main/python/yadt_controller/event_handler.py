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

from yadtbroadcastclient import WampBroadcaster
from twisted.internet import reactor
import logging
import sys

logger = logging.getLogger('event_handler')


class EventHandler(object):

    def _validate_port(self, port):
        if port < 0:
            error_message = 'port must be greater than 0, got {0}'.format(port)
            raise ValueError(error_message)

        if port > 65535:
            error_message = 'port {0} out of range, use port between 0 and 65535'.format(port)
            raise ValueError(error_message)

    def __init__(self, host, port, target):
        port = int(port)
        self._validate_port(port)
        self.host = host
        self.port = port
        self.target = target
        self.exit_code = None

    def initialize_for_info_request(self, timeout=5):
        self.wamp_broadcaster = WampBroadcaster(self.host, self.port, self.target)
        self.wamp_broadcaster.onEvent = self.on_info
        reactor.callWhenRunning(self.wamp_broadcaster.connect)
        reactor.callLater(timeout, self.on_info_timeout, timeout)
        reactor.run()
        sys.exit(self.exit_code)

    def initialize_for_execution_request(self, waiting_timeout=None, pending_timeout=None, command_to_execute=None,
                                         arguments=None):
        return None

    def on_info_timeout(self, timeout):
        logger.error('Timed out after %s seconds waiting for an info event.' % str(timeout))
        self.exit_code = 1
        reactor.stop()

    def on_info(self, target, info_event):
        logger.info(info_event)
        self.exit_code = 0
        reactor.stop()
