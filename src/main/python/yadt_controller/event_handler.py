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

from execution_state_machine import create_execution_state_machine_with_callbacks

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
                                         tracking_id=None):
        self.tracking_id = tracking_id
        self.waiting_timeout = waiting_timeout
        self.pending_timeout = pending_timeout
        self.command_to_execute = command_to_execute
        self.arguments = arguments

        self._prepare_broadcast_client()

        self.execution_state_machine = \
            create_execution_state_machine_with_callbacks(self.on_waiting_command_execution,
                                                          self.on_failed_command_execution,
                                                          self.on_pending_command_execution,
                                                          self.on_command_execution_success,
                                                          self.on_command_execution_failure,
                                                          self.on_execution_waiting_timeout,
                                                          self.on_execution_pending_timeout)
        self.wamp_broadcaster.onEvent = self.on_command_execution_event
        self.wamp_broadcaster.addOnSessionOpenHandler(self.publish_execution_request)
        reactor.callWhenRunning(self.wamp_broadcaster.connect)
        reactor.run()
        sys.exit(self.exit_code)

    def on_info_timeout(self, timeout):
        logger.error('Timed out after %s seconds waiting for an info event.' % str(timeout))
        self.exit_code = 1
        reactor.stop()

    def on_info(self, target, info_event):
        logger.info(info_event)
        self.exit_code = 0
        reactor.stop()

    def _prepare_broadcast_client(self):
        self.wamp_broadcaster = WampBroadcaster(self.host, self.port, self.target)

    def on_command_execution_event(self, target, event):
        if event.get('tracking_id') and event['tracking_id'] == self.tracking_id:
            payload = None
            if event.get('payload'):
                try:
                    payload = ' '.join(
                        ['%s=%s' % (key, value)
                         for d in event.get('payload')
                         for key, value in d.iteritems()])
                except Exception:
                    pass
            logger.info('Event "%s" received' % ' '.join(filter(None,
                                                                [event['id'],
                                                                 event.get('cmd'),
                                                                 event.get('state'),
                                                                 payload])))
            if event.get('state'):
                fun = getattr(self.execution_state_machine, event.get('state'))
                if fun:
                    previous_fsm_state = self.execution_state_machine.current
                    fun(msg=event['id'])
                    current_fsm_state = self.execution_state_machine.current
                    logger.debug('Transition from "{0}" to "{1}" since event "{2}" occured.'.format(previous_fsm_state,
                                                                                                    current_fsm_state,
                                                                                                    event['state']))

    def on_waiting_command_execution(self, event):
        reactor.callLater(self.waiting_timeout, self.execution_state_machine.waiting_timeout)

    def on_pending_command_execution(self, event):
        reactor.callLater(self.pending_timeout, self.execution_state_machine.pending_timeout)

    def on_failed_command_execution(self, event):
        if event.src == 'waiting':
            logger.warn('Command execution has not started yet, but got a failure event. Waiting for other receivers.')
        else:
            logger.error('The command failed.')

    def on_command_execution_success(self, event):
        self.exit_code = 0
        reactor.stop()

    def on_command_execution_failure(self, event):
        logger.error('Command execution failed.')
        self.exit_code = 1
        reactor.stop()

    def publish_execution_request(self):
        logger.debug('Publishing execution request : execute {0} on {1}'.format(self.command_to_execute, self.target))
        self.execution_state_machine.request(message='Execute {0} on {1}.'.format(self.command_to_execute, self.target))
        self.wamp_broadcaster.publish_request_for_target(self.target, self.command_to_execute, self.arguments)

    def on_execution_waiting_timeout(self, event):
        logger.error('Timed out waiting for the command execution to start.')

    def on_execution_pending_timeout(self, event):
        logger.error('Execution started and pending, but timed out while waiting for it to complete.')
