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


class RequestEmitter(object):

    def _validate_port(self, port):
        if type(port) != int:
            error_message = 'port must be an integer, got {0} instead'.format(type(port))
            raise ValueError(error_message)

        if port < 0:
            error_message = 'port must be greater than 0, got {0}'.format(port)
            raise ValueError(error_message)

        if port > 65535:
            error_message = 'port {0} out of range, use port between 0 and 65535'.format(port)
            raise ValueError(error_message)

    def __init__(self, host, port):
        self._validate_port(port)
        self.host = host
        self.port = port

    def initialize(self):
        wamp_broadcaster = WampBroadcaster(self.host, self.port)
        reactor.callWhenRunning(wamp_broadcaster.connect)
