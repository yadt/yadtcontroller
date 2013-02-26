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

import yadt_controller


class YadtControllerTests(unittest.TestCase):

    def setUp(self):
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({})
        when(yadt_controller.configuration).load(any_value()).thenReturn({'broadcaster_host': 'localhost',
                                                                          'broadcaster_port': 12345})
        when(yadt_controller).RequestEmitter(any_value(), any_value()).thenReturn(None)

    def tearDown(self):
        unstub()

    def test_should_parse_command_line_using_docopt_with_program_version_when_run(self):
        yadt_controller.run()

        verify(yadt_controller).docopt(yadt_controller.__doc__, version='${version}')

    def test_should_initialize_request_emitter_with_configuration(self):
        yadt_controller.run()

        verify(yadt_controller).RequestEmitter('localhost', 12345)

    def test_should_load_configuration_file_if_option_is_given(self):
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({'--config-file': '/path/to/config'})

        yadt_controller.run()

        verify(yadt_controller.configuration).load('/path/to/config')


    def test_should_load_default_configuration_file_if_option_is_not_given(self):
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({'--config-file': None})

        yadt_controller.run()

        verify(yadt_controller.configuration).load('/etc/yadtshell/controller.cfg')