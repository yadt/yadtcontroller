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
from mockito import when, unstub, verify

import yadt_controller
from yadt_controller.tracking import generate_tracking_id


class TrackingTests(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_generate_tracking_id_should_use_hostname_and_timestamp_and_target_for_generation(self):
        when(yadt_controller.tracking.getpass).getuser().thenReturn('user')
        when(yadt_controller.tracking.socket).getfqdn().thenReturn('host')
        when(yadt_controller.tracking).get_timestamp().thenReturn('timestamp')
        actual_tracking_id = generate_tracking_id('target')

        self.assertEqual('(timestamp):user@host->target', actual_tracking_id)

        verify(yadt_controller.tracking.getpass).getuser()
        verify(yadt_controller.tracking.socket).getfqdn()
        verify(yadt_controller.tracking).get_timestamp()
