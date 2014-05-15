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
        The event handler dispatches the events received from a YADT broadcaster
        and reacts accordingly. The protocol behaviour is dictated by an internal
        state machine.
        See https://raw.github.com/yadt/yadtreceiver/master/bigpicture.png for
        a big picture.
"""

from __future__ import print_function
from yadtbroadcastclient import WampBroadcaster
from twisted.internet import reactor
import logging
import sys

from execution_state_machine import create_execution_state_machine_with_callbacks

logger = logging.getLogger('event_handler')


class EventHandler(object):

    def _validate_port(self, port):
        if port < 0:
            error_message = 'port must be greater than 0, got {0}'.format(port)
            raise ValueError(error_message)

        if port > 65535:
            error_message = 'port {0} out of range, use port between 0 and 65535'.format(
                port)
            raise ValueError(error_message)

    def __init__(self, host, port, target):
        port = int(port)
        self._validate_port(port)
        self.host = host
        self.port = port
        self.target = target
        self.exit_code = None

    def initialize_for_info_request(self, timeout=5):
        self._prepare_broadcast_client()
        self.wamp_broadcaster.onEvent = self.on_info
        reactor.callWhenRunning(self.wamp_broadcaster.connect)
        reactor.callLater(timeout, self.on_info_timeout, timeout)
        reactor.run()
        sys.exit(self.exit_code)

    def initialize_for_execution_request(self, waiting_timeout=None,
                                         pending_timeout=None,
                                         command_to_execute=None,
                                         arguments=None,
                                         tracking_id=None,
                                         progress_handler=None):
        self.progress_handler = progress_handler
        self.tracking_id = tracking_id
        self.waiting_timeout = waiting_timeout
        self.pending_timeout = pending_timeout
        self.command_to_execute = command_to_execute
        self.arguments = arguments

        self._prepare_broadcast_client()

        self.execution_state_machine = \
            create_execution_state_machine_with_callbacks(
                self.on_waiting_command_execution,
                self.on_failed_command_execution,
                self.on_pending_command_execution,
                self.on_command_execution_success,
                self.on_command_execution_failure,
                self.on_execution_waiting_timeout,
                self.on_execution_pending_timeout)
        self.wamp_broadcaster.onEvent = self.on_command_execution_event
        self.wamp_broadcaster.addOnSessionOpenHandler(
            self.publish_execution_request)
        reactor.callLater(
            self.waiting_timeout, self.execution_state_machine.waiting_timeout)
        reactor.callWhenRunning(self.wamp_broadcaster.connect)
        reactor.run()
        sys.exit(self.exit_code)

    def on_info_timeout(self, timeout):
        logger.error(
            'Timed out after %s seconds waiting for an info event.' % str(timeout))
        self.exit_code = 1
        reactor.stop()

    def on_info(self, target, info_event):
        import json
        info_json = json.dumps(info_event)
        print(info_json)
        self.exit_code = 0
        reactor.stop()

    def on_command_execution_event(self, target, event):
        if event.get('tracking_id') != self.tracking_id:
            if event.get('state'):
                event_description = '{0} {1}'.format(
                    event.get('id'), event.get('state'))
            else:
                event_description = '{0}'.format(event.get('id'))
            logger.debug(
                'Ignoring event {0} with a foreign tracking ID: {1}.'.format(event_description,
                                                                             event.get('tracking_id')))
            return

        try:
            self._pretty_print_event(event)
            self._output_error_report(event)
            self._output_call_info(event)
            self._output_service_change(event)
            self._apply_state_transition_to_state_machine(event)
        except Exception as e:
            logger.debug("Error while processing event : %s" % e)

    def on_waiting_command_execution(self, event):
        pass

    def on_pending_command_execution(self, event):
        if self.progress_handler:
            self.progress_handler.output_progress(
                sys.stdout, '{0} started'.format(self.arguments[0]))
        reactor.callLater(
            self.pending_timeout, self.execution_state_machine.pending_timeout)

    def on_failed_command_execution(self, event):
        if event.src == 'waiting':
            logger.warn(
                'Command execution has not started yet, but got a failure event. Waiting for other receivers.')
        else:
            logger.error('The command failed.')

    def on_command_execution_success(self, event):
        if self.progress_handler:
            self.progress_handler.output_progress(
                sys.stdout, '{0} successful'.format(self.arguments[0]))
        self.exit_code = 0
        reactor.stop()

    def on_command_execution_failure(self, event):
        if self.progress_handler:
            self.progress_handler.output_progress(
                sys.stdout, '{0} failed'.format(self.arguments[0]))
        logger.debug('Waiting for possible error reports from a receiver..')
        self.exit_code = 1
        reactor.callLater(10, reactor.stop)

    def publish_execution_request(self):
        logger.debug('Publishing execution request : execute {0} on {1}'.format(
            self.command_to_execute, self.target))
        self.execution_state_machine.request(
            message='Execute {0} on {1}.'.format(self.command_to_execute, self.target))
        self.wamp_broadcaster.publish_request_for_target(
            self.target, self.command_to_execute, self.arguments)

    def on_execution_waiting_timeout(self, event):
        logger.error('Did not get any response from a yadt receiver - '
                     'the command "{0} {1}" was not started within {2} seconds'.format(self.command_to_execute,
                                                                                       ' '.join(self.arguments),
                                                                                       self.waiting_timeout))

    def on_execution_pending_timeout(self, event):
        logger.error('Execution of "{0} {1}" started and pending, but timed out after {2} seconds '
                     'while waiting for it to complete.'.format(self.command_to_execute,
                                                                ' '.join(self.arguments),
                                                                self.pending_timeout))

    def _prepare_broadcast_client(self):
        self.wamp_broadcaster = WampBroadcaster(
            self.host, self.port, self.target)

    def _output_service_change(self, event):
        if event.get('id') == 'service-change' and event.get('payload'):
            for service_change in event.get('payload'):
                message = '{0} is now {1}.'.format(
                    service_change.get('uri'), service_change.get('state'))
                logger.info(message)
                if self.progress_handler is not None:
                    self.progress_handler.output_progress(sys.stdout, message)

    def _output_error_report(self, event):
        if self._event_is_an_error_report(event):
            logger.error('*' * 5 + 'Error report' + '*' * 5)
            for error_message_line in event.get('message').split('\n'):
                logger.error(error_message_line)

    def _event_is_an_error_report(self, event):
        return event.get('id') == 'cmd' and event.get('state') == 'failed' and event.get('message')

    def _output_call_info(self, event):
        if self._event_is_a_call_info(event):
            logger.info(' Affected target: %s' % event.get('target'))
            logger.info(' Host executing the command: %s' % event.get('host'))
            logger.info(' Logfile on %s is at : %s' % (event.get('host'), event.get('log_file')))

    def _event_is_a_call_info(self, event):
        return event.get('id') == 'call-info'

    def _apply_state_transition_to_state_machine(self, event):
        if event.get('state'):
            fun = getattr(self.execution_state_machine, event.get('state'))
            if fun:
                previous_fsm_state = self.execution_state_machine.current
                fun(msg=event['id'])
                current_fsm_state = self.execution_state_machine.current
                logger.debug(
                    'Transition from "{0}" to "{1}" since event "{2}" occured.'.format(previous_fsm_state,
                                                                                       current_fsm_state,
                                                                                       event['state']))

    def _pretty_print_event(self, event):
        payload = None
        try:
            if event.get('payload'):
                payload = ' '.join(
                    ['%s=%s' % (key, value)
                     for d in event.get('payload')
                     for key, value in d.iteritems()])
        except:
            pass
        logger.debug('Event "%s" received' % ' '.join(filter(None,
                                                             [event['id'],
                                                              event.get('cmd'),
                                                              event.get(
                                                                  'state'),
                                                              payload])))
