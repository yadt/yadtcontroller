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
from mockito import when, verify, unstub, any as any_value, mock

from yadt_controller.request_emitter import RequestEmitter


class RequestEmitterTests(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_should_instantiate_request_emitter_with_host_and_port(self):
        request_emitter = RequestEmitter('host', 8081)

        self.assertEqual(request_emitter.host, 'host')
        self.assertEqual(request_emitter.port, 8081)

    def test_should_raise_exception_when_port_is_not_an_integer(self):
        self.assertRaises(ValueError, RequestEmitter, 'host', 'notaninteger')

    def test_should_raise_exception_when_port_is_negative(self):
        self.assertRaises(ValueError, RequestEmitter, 'host', -80)

    def test_should_raise_exception_if_port_is_greater_than_65535(self):
        self.assertRaises(ValueError, RequestEmitter, 'host', 65536)