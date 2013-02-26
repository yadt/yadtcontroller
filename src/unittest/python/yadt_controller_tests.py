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
from mockito import when, verify, unstub, any as any_value, mock, never

import yadt_controller
from yadt_controller.request_emitter import RequestEmitter


class YadtControllerTests(unittest.TestCase):

    def setUp(self):
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({})
        when(yadt_controller).load(any_value()).thenReturn({'broadcaster-host': 'localhost',
                                                                          'broadcaster-port': 12345})
        self.request_emitter_mock = mock(RequestEmitter)
        when(yadt_controller).RequestEmitter(any_value(), any_value()).thenReturn(self.request_emitter_mock)

    def tearDown(self):
        unstub()

    def test_should_parse_command_line_using_docopt_with_program_version_when_run(self):
        yadt_controller.run()

        verify(yadt_controller).docopt(yadt_controller.__doc__, version='${version}')

    def test_should_initialize_request_emitter_with_default_configuration(self):
        yadt_controller.run()

        verify(yadt_controller).RequestEmitter('localhost', 12345)

    def test_should_initialize_request_emitter_with_provided_host(self):
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({'--broadcaster-host': 'host'})

        yadt_controller.run()

        verify(yadt_controller).RequestEmitter('host', 12345)

    def test_should_initialize_request_emitter_with_provided_port(self):
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({'--broadcaster-port': 54321})

        yadt_controller.run()

        verify(yadt_controller).RequestEmitter('localhost', 54321)



    def test_should_load_configuration_file_if_option_is_given(self):
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({'--config-file': '/path/to/config',
                                                                                   '--broadcaster-host': None})

        yadt_controller.run()

        verify(yadt_controller).load('/path/to/config')


    def test_should_load_default_configuration_file_if_option_is_not_given(self):
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({'--broadcaster-host': None})

        yadt_controller.run()

        verify(yadt_controller).load('/etc/yadtshell/controller.cfg')


    def test_should_initialize_request_emitter_upon_calling_run(self):
        yadt_controller.run()

        verify(self.request_emitter_mock).initialize()