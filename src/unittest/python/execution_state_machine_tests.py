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

from yadt_controller.execution_state_machine import create_execution_state_machine_with_callbacks


class ExecutionStateMachineTests(unittest.TestCase):
    calls = []

    def setUp(self):
        self.calls = []

    def waiting_callback(self):
        self.calls.append("waiting")

    def failed_callback(self):
        self.calls.append("failed")

    def pending_callback(self):
        self.calls.append("pending")

    def success_callback(self):
        self.calls.append("success")

    def failure_callback(self):
        self.calls.append("failure")

    def waiting_timeout_callback(self):
        self.calls.append("waiting_timeout")

    def pending_timeout_callback(self):
        self.calls.append("pending_timeout")

    def test_should_create_state_machine_with_callbacks(self):
        fsm = create_execution_state_machine_with_callbacks(
            waiting_callback=self.waiting_callback,
            failed_callback=self.failed_callback,
            pending_callback=self.pending_callback,
            success_callback=self.success_callback,
            failure_callback=self.failure_callback,
            waiting_timeout_callback=self.waiting_timeout_callback,
            pending_timeout_callback=self.pending_timeout_callback)

        fsm.onwaiting()
        fsm.onfailed()
        fsm.onpending()
        fsm.onsuccess()
        fsm.onfailure()
        fsm.onwaiting_timeout()
        fsm.onpending_timeout()

        self.assertEqual(
            self.calls, 
            ['waiting',
             'failed',
             'pending',
             'success',
             'failure',
             'waiting_timeout',
             'pending_timeout'])

    def test_state_machine_should_be_in_idle_state_initially(self):
        fsm = create_execution_state_machine_with_callbacks(
            waiting_callback=self.waiting_callback,
            failed_callback=self.failed_callback,
            pending_callback=self.pending_callback,
            success_callback=self.success_callback,
            failure_callback=self.failure_callback,
            waiting_timeout_callback=self.waiting_timeout_callback,
            pending_timeout_callback=self.pending_timeout_callback)

        self.assertEqual(fsm.current, 'idle')

    def test_should_not_fail_with_stacktrace_when_request_publishing_takes_too_long(self):
        id = lambda x: x
        fsm = create_execution_state_machine_with_callbacks(id, id, id, id, id, id, id)
        fsm.waiting_timeout()
        fsm.request()
        self.assertEqual(fsm.current, 'failure')

    def test_should_not_fail_with_stacktrace_timing_out_after_success(self):
        id = lambda x: x
        fsm = create_execution_state_machine_with_callbacks(id, id, id, id, id, id, id)
        fsm.request()
        fsm.started()
        fsm.finished()
        fsm.waiting_timeout()
        self.assertEqual(fsm.current, 'success')
