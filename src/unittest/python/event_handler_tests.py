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

    def test_should_instantiate_event_handler_with_host_and_port(self):
        event_handler = EventHandler('host', 8081, 'target')

        self.assertEqual(event_handler.host, 'host')
        self.assertEqual(event_handler.port, 8081)
        self.assertEqual(event_handler.target, 'target')

    def test_should_exit_with_error_when_info_request_times_out(self):
        event_handler = EventHandler('host', 8081, 'target')
        when(yadt_controller.event_handler.reactor).stop().thenReturn(None)
        when(yadt_controller.event_handler.logger).error(any_value()).thenReturn(None)

        event_handler.on_info_timeout(10)

        self.assertEqual(event_handler.exit_code, 1)
        verify(yadt_controller.event_handler.reactor).stop()

    def test_should_raise_exception_when_port_is_not_an_integer(self):
        self.assertRaises(ValueError, EventHandler, 'host', 'notaninteger', 'target')

    def test_should_raise_exception_when_port_is_negative(self):
        self.assertRaises(ValueError, EventHandler, 'host', -80, 'target')

    def test_should_raise_exception_if_port_is_greater_than_65535(self):
        self.assertRaises(ValueError, EventHandler, 'host', 65536, 'target')

    def test_should_create_event_handler_with_configuration(self):
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).callLater(any_value(), any_value(), any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)
        when(yadt_controller.event_handler.sys).exit(any_value()).thenReturn(None)

        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_info_request()

        verify(yadt_controller.event_handler).WampBroadcaster('hostname', 12345, 'target')

    def test_should_add_connect_callback_to_reactor(self):
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).callLater(any_value(), any_value(), any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)
        when(yadt_controller.event_handler.sys).exit(any_value()).thenReturn(None)

        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_info_request()

        verify(yadt_controller.event_handler.reactor).callWhenRunning(self.wampbroadcaster.connect)

    def test_should_set_onevent_callback_when_initializing_wamp_broadcaster(self):
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).callLater(any_value(), any_value(), any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)
        when(yadt_controller.event_handler.sys).exit(any_value()).thenReturn(None)

        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_info_request()

        self.assertTrue(event_handler.wamp_broadcaster.onEvent == event_handler.on_info)

    def test_should_set_schedule_timeout_when_initializing_wamp_broadcaster_for_info(self):
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.sys).exit(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).callLater(any_value(), any_value(), any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).callLater(any_value(), any_value(), any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)

        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_info_request(timeout=10)

        verify(yadt_controller.event_handler.reactor).callLater(10, event_handler.on_info_timeout, 10)

    def test_oninfo_should_stop_reactor(self):
        when(yadt_controller.event_handler.reactor).stop().thenReturn(None)
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).callLater(any_value(), any_value(), any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)

        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.on_info('some-target', 'an-info-event')

        verify(yadt_controller.event_handler.reactor).stop()


    def test_should_start_reactor(self):
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).callLater(any_value(), any_value(), any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)
        when(yadt_controller.event_handler.sys).exit(any_value()).thenReturn(None)

        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_info_request()

        verify(yadt_controller.event_handler.reactor).run()