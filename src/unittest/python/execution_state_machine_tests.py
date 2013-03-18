import unittest
from yadt_controller.execution_state_machine import create_execution_state_machine_with_callbacks


class ExecutionStateMachineTests(unittest.TestCase):

    def waiting_callback(self):
        pass

    def failed_callback(self):
        pass

    def pending_callback(self):
        pass

    def success_callback(self):
        pass

    def failure_callback(self):
        pass

    def waiting_timeout_callback(self):
        pass

    def pending_timeout_callback(self):
        pass

    def test_should_create_state_machine_with_callbacks(self):
        fsm = create_execution_state_machine_with_callbacks(waiting_callback=self.waiting_callback,
                                                            failed_callback=self.failed_callback,
                                                            pending_callback=self.pending_callback,
                                                            success_callback=self.success_callback,
                                                            failure_callback=self.failure_callback,
                                                            waiting_timeout_callback=self.waiting_timeout_callback,
                                                            pending_timeout_callback=self.pending_timeout_callback)

        self.assertEqual(fsm.onwaiting, self.waiting_callback)
        self.assertEqual(fsm.onfailed, self.failed_callback)
        self.assertEqual(fsm.onpending, self.pending_callback)
        self.assertEqual(fsm.onsuccess, self.success_callback)
        self.assertEqual(fsm.onfailure, self.failure_callback)

    def test_state_machine_should_be_in_idle_state_initially(self):
        fsm = create_execution_state_machine_with_callbacks(waiting_callback=self.waiting_callback,
                                                            failed_callback=self.failed_callback,
                                                            pending_callback=self.pending_callback,
                                                            success_callback=self.success_callback,
                                                            failure_callback=self.failure_callback,
                                                            waiting_timeout_callback=self.waiting_timeout_callback,
                                                            pending_timeout_callback=self.pending_timeout_callback)

        self.assertEqual(fsm.current, 'idle')