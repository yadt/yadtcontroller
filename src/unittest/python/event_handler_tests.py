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
from mockito import when, verify, unstub, any as any_value, mock, never
import yadt_controller.configuration
from yadt_controller.event_handler import EventHandler


class EventHandlerTests(unittest.TestCase):

    def setUp(self):
        self.wampbroadcaster = mock(WampBroadcaster)
        self.wampbroadcaster.connect = lambda: None
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).callLater(any_value(), any_value(), any_value()).thenReturn(None)
        when(yadt_controller.event_handler).WampBroadcaster(any_value(),
                                                            any_value(),
                                                            any_value()).thenReturn(self.wampbroadcaster)
        when(yadt_controller.event_handler.logger).info(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.logger).debug(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.logger).error(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.logger).warn(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.sys).exit(any_value()).thenReturn(None)

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
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)
        when(yadt_controller.event_handler.sys).exit(any_value()).thenReturn(None)

        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_info_request()

        verify(yadt_controller.event_handler).WampBroadcaster('hostname', 12345, 'target')

    def test_should_add_connect_callback_to_reactor(self):
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)
        when(yadt_controller.event_handler.sys).exit(any_value()).thenReturn(None)

        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_info_request()

        verify(yadt_controller.event_handler.reactor).callWhenRunning(self.wampbroadcaster.connect)

    def test_should_set_onevent_callback_when_initializing_wamp_broadcaster(self):
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)
        when(yadt_controller.event_handler.sys).exit(any_value()).thenReturn(None)

        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_info_request()

        self.assertTrue(event_handler.wamp_broadcaster.onEvent == event_handler.on_info)

    def test_should_set_schedule_timeout_when_initializing_wamp_broadcaster_for_info(self):
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.sys).exit(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)

        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_info_request(timeout=10)

        verify(yadt_controller.event_handler.reactor).callLater(10, event_handler.on_info_timeout, 10)

    def test_oninfo_should_stop_reactor(self):
        when(yadt_controller.event_handler.reactor).stop().thenReturn(None)
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)


        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.on_info('some-target', 'an-info-event')

        verify(yadt_controller.event_handler.reactor).stop()


    def test_should_start_reactor(self):
        when(yadt_controller.event_handler.reactor).callWhenRunning(any_value()).thenReturn(None)
        when(yadt_controller.event_handler.reactor).run().thenReturn(None)
        when(yadt_controller.event_handler.sys).exit(any_value()).thenReturn(None)

        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_info_request()

        verify(yadt_controller.event_handler.reactor).run()

    def test_should_prepare_broadcast_client_when_requesting_execution(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        when(event_handler)._prepare_broadcast_client().thenReturn(None)
        event_handler.wamp_broadcaster = mock()

        event_handler.initialize_for_execution_request()

        verify(event_handler)._prepare_broadcast_client()

    def test_should_create_execution_state_machine_for_command_execution(self):
        mock_state_machine = mock()
        when(yadt_controller.event_handler).\
            create_execution_state_machine_with_callbacks(any_value(),
                                                          any_value(),
                                                          any_value(),
                                                          any_value(),
                                                          any_value(),
                                                          any_value(),
                                                          any_value()).thenReturn(mock_state_machine)
        event_handler = EventHandler('hostname', 12345, 'target')

        event_handler.initialize_for_execution_request()

        self.assertTrue(event_handler.execution_state_machine is mock_state_machine)

    def test_should_set_broadcast_client_onEvent_when_initializing_command_execution(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_execution_request()

        self.assertEqual(event_handler.on_command_execution_event, event_handler.wamp_broadcaster.onEvent)

    def test_should_add_session_open_handler_to_broadcast_client_when_initializing_command_execution(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        when(event_handler)._prepare_broadcast_client().thenReturn(None)
        mock_broadcaster = mock()
        event_handler.wamp_broadcaster = mock_broadcaster
        when(mock_broadcaster).addOnSessionOpenHandler(any_value()).thenReturn(None)

        event_handler.initialize_for_execution_request()

        verify(mock_broadcaster).addOnSessionOpenHandler(event_handler.publish_execution_request)

    def test_should_log_error_when_waiting_execution_request_times_out(self):
        event_handler = EventHandler('host', 8081, 'target')
        when(yadt_controller.event_handler.reactor).stop().thenReturn(None)
        when(yadt_controller.event_handler.logger).error(any_value()).thenReturn(None)

        event_handler.on_execution_waiting_timeout(mock())

        verify(yadt_controller.event_handler.logger).error('Timed out waiting for the command execution to start.')

    def test_should_log_error_when_pending_execution_request_times_out(self):
        event_handler = EventHandler('host', 8081, 'target')
        when(yadt_controller.event_handler.reactor).stop().thenReturn(None)
        when(yadt_controller.event_handler.logger).error(any_value()).thenReturn(None)

        event_handler.on_execution_pending_timeout(mock())

        verify(yadt_controller.event_handler.logger).error('Execution started and pending, but timed out while waiting '
                                                           'for it to complete.')

    def test_publish_execution_request_should_trigger_request_event_on_state_machine(self):
        event_handler = EventHandler('host', 8081, 'target')
        event_handler.initialize_for_execution_request()

        event_handler.publish_execution_request()

        self.assertEqual(event_handler.execution_state_machine.current, 'waiting')

    def test_publish_execution_request_should_trigger_broadcaster_publish(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        when(event_handler)._prepare_broadcast_client().thenReturn(None)
        mock_broadcaster = mock()
        event_handler.wamp_broadcaster = mock_broadcaster
        event_handler.initialize_for_execution_request(command_to_execute='command', arguments=['arg1', 'arg2'])

        event_handler.publish_execution_request()

        verify(mock_broadcaster).publish_request_for_target('target', 'command', ['arg1', 'arg2'])

    def test_should_stop_reactor_and_set_exit_code_when_command_execution_was_sucessful(self):
        when(yadt_controller.event_handler.reactor).stop().thenReturn(None)
        event_handler = EventHandler('hostname', 12345, 'target')

        event_handler.on_command_execution_success(mock())

        self.assertEqual(event_handler.exit_code, 0)
        verify(yadt_controller.event_handler.reactor).stop()

    def test_should_stop_reactor_and_set_exit_code_when_command_execution_was_failed(self):
        when(yadt_controller.event_handler.reactor).stop().thenReturn(None)
        when(yadt_controller.event_handler.logger).error(any_value()).thenReturn(None)
        event_handler = EventHandler('hostname', 12345, 'target')

        event_handler.on_command_execution_failure(mock())

        self.assertEqual(event_handler.exit_code, 1)
        verify(yadt_controller.event_handler.reactor).callLater(10, yadt_controller.event_handler.reactor.stop)

    def test_on_waiting_command_execution_should_schedule_waiting_timeout(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_execution_request(waiting_timeout=10)
        event_handler.on_waiting_command_execution(mock())

        verify(yadt_controller.event_handler.reactor).callLater(10,
                                                                event_handler.execution_state_machine.waiting_timeout)

    def test_on_pending_command_execution_should_schedule_pending_timeout(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_execution_request(pending_timeout=5)
        event_handler.on_pending_command_execution(mock())

        verify(yadt_controller.event_handler.reactor).callLater(5,
                                                                event_handler.execution_state_machine.pending_timeout)

    def test_on_failed_command_execution_should_ignore_failures_if_command_has_not_started_yet(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_execution_request()
        mock_event = mock()
        mock_event.src = 'waiting'
        when(yadt_controller.event_handler.logger).warn(any_value()).thenReturn(None)

        event_handler.on_failed_command_execution(mock_event)

        verify(yadt_controller.event_handler.logger).warn('Command execution has not started yet, but got a failure '
                                                          'event. Waiting for other receivers.')

    def test_on_failed_command_execution_should_log_error_if_command_has_started(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.initialize_for_execution_request()
        mock_event = mock()
        mock_event.src = 'pending'
        when(yadt_controller.event_handler.logger).error(any_value()).thenReturn(None)

        event_handler.on_failed_command_execution(mock_event)

        verify(yadt_controller.event_handler.logger).error('The command failed.')

    def test_should_schedule_broadcaster_connect_when_initializing_command_execution(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        when(event_handler)._prepare_broadcast_client().thenReturn(None)
        mock_broadcaster = mock()
        mock_broadcaster.connect = lambda: None

        event_handler.wamp_broadcaster = mock_broadcaster
        event_handler.initialize_for_execution_request()

        verify(yadt_controller.event_handler.reactor).callWhenRunning(event_handler.wamp_broadcaster.connect)

    def test_on_command_execution_event_should_log_payload_if_present(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.tracking_id = '123'
        event={'id': 'service-change',
               'type': 'event',
               'target': 'target',
               'tracking_id': '123',
               'payload': [{'state': 'up',
                            'uri': 'service://host/service'}]}

        event_handler.on_command_execution_event('target', event)

        verify(yadt_controller.event_handler.logger).\
            debug('Event "service-change state=up uri=service://host/service" received')

    def test_on_command_execution_event_should_log_error_abstract(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.tracking_id = '123'
        mock_state_machine = mock()
        event_handler.execution_state_machine = mock_state_machine
        when(mock_state_machine).test_state(msg=any_value()).thenReturn(None)
        event={'id': 'cmd',
               'type': 'event',
               'target': 'target',
               'tracking_id': '123',
               'state': 'failed',
               'message': 'The internet was shut down.\nSeriously.'}

        event_handler.on_command_execution_event('target', event)

        verify(yadt_controller.event_handler.logger). \
            error('The internet was shut down.')
        verify(yadt_controller.event_handler.logger). \
            error('Seriously.')

    def test_on_command_execution_event_should_not_do_anything_if_tracking_id_does_not_match(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.tracking_id = 'something-else'
        event={'id': 'service-change',
               'type': 'event',
               'target': 'target',
               'tracking_id': '123',
               'payload': [{'state': 'up',
                            'uri': 'service://host/service'}]}

        event_handler.on_command_execution_event('target', event)

        verify(yadt_controller.event_handler.logger, never). \
            info('Event "service-change state=up uri=service://host/service" received')

    def test_on_command_execution_event_should_eat_exceptions_from_malformed_events(self):
        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.tracking_id = 'test'
        malformed_event = {'id': 'service-change',
                           'type': 'event',
                           'tracking_id': 'test',
                           'payload': {
                               'state': 1,  # blows up if uncaught
                               'uri': 'service://host/service'}}

        event_handler.on_command_execution_event('target', malformed_event)

    def test_on_command_execution_event_should_call_state_machine_transition_when_state_change_occurs(self):
        mock_state_machine = mock()
        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.tracking_id = '123'
        event_handler.execution_state_machine = mock_state_machine
        when(mock_state_machine).test_state(msg=any_value()).thenReturn(None)

        event = {'cmd': 'update',
                 'state': 'test_state',
                 'tracking_id': '123',
                 'message': None,
                 'type': 'event',
                 'id': 'cmd'}
        event_handler.on_command_execution_event('target', event)

        verify(mock_state_machine).test_state(msg='cmd')

    def test_on_command_execution_event_should_not_call_state_machine_transition_when_id_does_not_match(self):
        mock_state_machine = mock()
        event_handler = EventHandler('hostname', 12345, 'target')
        event_handler.tracking_id = 'something-else'
        event_handler.execution_state_machine = mock_state_machine
        when(mock_state_machine).test_state(msg=any_value()).thenReturn(None)

        event = {'cmd': 'update',
                 'state': 'test_state',
                 'tracking_id': '123',
                 'message': None,
                 'type': 'event',
                 'id': 'cmd'}
        event_handler.on_command_execution_event('target', event)

        verify(mock_state_machine, never).test_state(msg='cmd')