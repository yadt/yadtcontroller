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

import unittest
from yadtbroadcastclient import WampBroadcaster
from mockito import when, verify, unstub, any as any_value, mock
import yadt_controller.configuration
from yadt_controller.event_handler import EventHandler


class RequestEmitterTests(unittest.TestCase):

    def setUp(self):
        self.wampbroadcaster = mock(WampBroadcaster)
        self.wampbroadcaster.connect = lambda: None
        when(yadt_controller.event_handler).WampBroadcaster(any_value(), any_value(), any_value()).thenReturn(self.wampbroadcaster)

    def tearDown(self):
        unstub()

    def test_should_instantiate_request_emitter_with_host_and_port(self):
        request_emitter = EventHandler('host', 8081, 'target')

        self.assertEqual(request_emitter.host, 'host')
        self.assertEqual(request_emitter.port, 8081)
        self.assertEqual(request_emitter.target, 'target')

    def test_should_raise_exception_when_port_is_not_an_integer(self):
        self.assertRaises(ValueError, EventHandler, 'host', 'notaninteger', 'target')

    def test_should_raise_exception_when_port_is_negative(self):
        self.assertRaises(ValueError, EventHandler, 'host', -80, 'target')

    def test_should_raise_exception_if_port_is_greater_than_65535(self):
        self.assertRaises(ValueError, EventHandler, 'host', 65536, 'target')

    def test_should_create_request_emitter_with_configuration(self):
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)

        request_emitter = EventHandler('hostname', 12345, 'target')
        request_emitter.initialize()

        verify(yadt_controller.event_handler).WampBroadcaster('hostname', 12345, 'target')

    def test_should_add_connect_callback_to_reactor(self):
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)

        request_emitter = EventHandler('hostname', 12345, 'target')
        request_emitter.initialize()

        verify(yadt_controller.event_handler.reactor).callWhenRunning(self.wampbroadcaster.connect)

    def test_should_start_reactor(self):
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)

        request_emitter = EventHandler('hostname', 12345, 'target')
        request_emitter.initialize()

        verify(yadt_controller.event_handler.reactor).run()