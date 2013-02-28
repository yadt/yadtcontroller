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
from docopt import Option

import yadt_controller
from yadt_controller.event_handler import EventHandler


class YadtControllerTests(unittest.TestCase):

    def setUp(self):
        when(yadt_controller).basicConfig(format=any_value()).thenReturn(None)
        self.mock_root_logger = mock()
        when(yadt_controller).getLogger().thenReturn(self.mock_root_logger)
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({'<target>': 'target',
                                                                                   '--config-file': '/path/to/config',
                                                                                   '--broadcaster-host': 'host',
                                                                                   '--broadcaster-port': '54321'})
        when(yadt_controller).load(any_value()).thenReturn({'broadcaster-host': 'localhost',
                                                                                'broadcaster-port': 12345})
        self.request_emitter_mock = mock(EventHandler)
        when(yadt_controller).EventHandler(any_value(), any_value(), any_value()).thenReturn(self.request_emitter_mock)

    def tearDown(self):
        unstub()

    def test_should_initialize_logging(self):
        yadt_controller.run()

        verify(yadt_controller).basicConfig(format='[%(levelname)s] %(message)s')
        verify(yadt_controller).getLogger()
        verify(self.mock_root_logger).setLevel(yadt_controller.INFO)

    def test_should_parse_command_line_using_docopt_with_program_version_when_run(self):
        yadt_controller.run()

        verify(yadt_controller).docopt(yadt_controller.__doc__, version='${version}')

    def test_should_initialize_request_emitter_with_provided_host_and_port(self):
        yadt_controller.run()

        verify(yadt_controller).EventHandler('host', '54321', 'target')

    def test_should_load_configuration_file(self):
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({'--config-file': '/configuration',
                                                                                   '--broadcaster-host': None,
                                                                                   '<target>': 'target',
                                                                                   '--broadcaster-port': '1234'})
        yadt_controller.run()

        verify(yadt_controller).load('/configuration')

    def test_should_initialize_request_emitter_upon_calling_run(self):
        yadt_controller.run()

        verify(self.request_emitter_mock).initialize()

    def test_determine_configuration_should_not_override_broadcaster_host_from_config_file_with_default(self):
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({'--config-file': '/configuration',
                                                                                   '--broadcaster-host': 'default-host',
                                                                                   '<target>': 'target',
                                                                                   '--broadcaster-port': '1234'})
        when(yadt_controller).parse_defaults(yadt_controller.__doc__).thenReturn([Option('-p',
                                                                                         '--broadcaster-port',
                                                                                         1,
                                                                                         'default-port'),
                                                                                  Option('-b',
                                                                                         '--broadcaster-host',
                                                                                         1,
                                                                                         'default-host')])
        yadt_controller.run()

        verify(yadt_controller).EventHandler('localhost', '1234', 'target')

    def test_determine_configuration_should_not_override_broadcaster_port_from_config_file_with_default(self):
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({'--config-file': '/configuration',
                                                                                   '--broadcaster-host': 'host',
                                                                                   '<target>': 'target',
                                                                                   '--broadcaster-port': 'default-port'})
        when(yadt_controller).parse_defaults(yadt_controller.__doc__).thenReturn([Option('-p',
                                                                                         '--broadcaster-port',
                                                                                         1,
                                                                                         'default-port'),
                                                                                  Option('-b',
                                                                                         '--broadcaster-host',
                                                                                         1,
                                                                                         'default-host')])
        yadt_controller.run()

        verify(yadt_controller).EventHandler('host', 12345, 'target')

    def test_get_defaults_should_return_default_broadcaster_and_port(self):
        when(yadt_controller).parse_defaults(yadt_controller.__doc__).thenReturn([Option('-p',
                                                                                         '--broadcaster-port',
                                                                                         1,
                                                                                         'default-port'),
                                                                                  Option('-b',
                                                                                         '--broadcaster-host',
                                                                                         1,
                                                                                         'default-host')])

        actual_defaults = yadt_controller._get_defaults()

        self.assertEqual(actual_defaults, {'--broadcaster-host': 'default-host',
                                           '--broadcaster-port': 'default-port'})