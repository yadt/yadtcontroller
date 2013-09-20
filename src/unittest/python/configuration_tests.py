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


__author__ = 'Marcel Wolf, Michael Gruber'

import unittest

from mock import Mock, call, patch

from yadt_controller.configuration import (SECTION_BROADCASTER,
                                           ControllerConfigLoader,
                                           load)
from yadtcommons.configuration import YadtConfigParser, ConfigurationException


class ControllerConfigLoaderTests (unittest.TestCase):

    def test_should_create_instance_of_SafeConfigParser(self):
        parser = ControllerConfigLoader()

        name_of_type = parser._parser.__class__.__name__
        self.assertEqual('YadtConfigParser', name_of_type)

    def test_should_use_provided_defaults(self):
        loader = ControllerConfigLoader({'--broadcaster-host': 'default-host',
                                         '--broadcaster-port': 'default-port'})
        self.assertEqual(loader.DEFAULT_BROADCASTER_HOST, 'default-host')
        self.assertEqual(loader.DEFAULT_BROADCASTER_PORT, 'default-port')

    def test_should_return_broadcaster_host_option(self):
        mock_loader = Mock(ControllerConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = 'broadcaster.host'
        mock_loader._parser = mock_parser

        actual_broadcaster_host = ControllerConfigLoader.get_broadcaster_host(
            mock_loader)

        self.assertEqual('broadcaster.host', actual_broadcaster_host)
        self.assertEqual(
            call(SECTION_BROADCASTER, 'host', mock_loader.DEFAULT_BROADCASTER_HOST), mock_parser.get_option.call_args)

    def test_should_return_broadcaster_port_option(self):
        mock_loader = Mock(ControllerConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option_as_int.return_value = 8081
        mock_loader._parser = mock_parser

        actual_broadcaster_port = ControllerConfigLoader.get_broadcaster_port(
            mock_loader)

        self.assertEqual(8081, actual_broadcaster_port)
        self.assertEqual(
            call(SECTION_BROADCASTER, 'port', mock_loader.DEFAULT_BROADCASTER_PORT), mock_parser.get_option_as_int.call_args)

    def test_should_delegate_read_configuration_file(self):
        mock_loader = Mock(ControllerConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.read_configuration_file.return_value = {'spam': 'eggs'}
        mock_loader._parser = mock_parser

        actual_configuration = ControllerConfigLoader.read_configuration_file(
            mock_loader, 'filename.cfg')

        self.assertEqual({'spam': 'eggs'}, actual_configuration)
        self.assertEqual(
            call('filename.cfg'), mock_parser.read_configuration_file.call_args)


class LoadTest (unittest.TestCase):

    @patch('yadt_controller.configuration.ControllerConfigLoader')
    def test_should_load_configuration_from_file(self, mock_loader_class):
        mock_loader = Mock(ControllerConfigLoader)
        mock_loader_class.return_value = mock_loader

        load('abc')

        self.assertEqual(
            call('abc'), mock_loader.read_configuration_file.call_args)

    @patch('yadt_controller.configuration.ControllerConfigLoader')
    def test_should_load_defaults(self, mock_loader):
        mock_defaults = Mock()

        load('abc', mock_defaults)

        self.assertEqual(call(mock_defaults), mock_loader.call_args)

    @patch('yadt_controller.configuration.logger')
    @patch('yadt_controller.configuration.ControllerConfigLoader')
    def test_should_ignore_configuration_exception(self, mock_loader_class, mock_logger):
        mock_loader = Mock(ControllerConfigLoader)
        mock_loader.read_configuration_file.side_effect = ConfigurationException(
            'bla')
        mock_loader_class.return_value = mock_loader

        load('/foo/bar')

    @patch('yadt_controller.configuration.ControllerConfigLoader')
    def test_should_get_broadcaster_properties_from_parser(self, mock_loader_class):
        mock_loader = Mock(ControllerConfigLoader)
        mock_loader.get_broadcaster_host.return_value = 'broadcaster host'
        mock_loader.get_broadcaster_port.return_value = 12345
        mock_loader_class.return_value = mock_loader

        actual_configuration = load('abc')

        self.assertEqual(call(), mock_loader.get_broadcaster_host.call_args)
        self.assertEqual(
            'broadcaster host', actual_configuration['broadcaster-host'])

        self.assertEqual(call(), mock_loader.get_broadcaster_port.call_args)
        self.assertEqual(12345, actual_configuration['broadcaster-port'])

    @patch('yadt_controller.configuration.ControllerConfigLoader')
    def test_should_get_receiver_properties_from_parser(self, mock_loader_class):
        mock_loader = Mock(ControllerConfigLoader)
        mock_loader.get_broadcaster_host.return_value = 'broadcaster host name'
        mock_loader.get_broadcaster_port.return_value = 12345
        mock_loader_class.return_value = mock_loader

        actual_configuration = load('abc')

        self.assertEqual(call(), mock_loader.get_broadcaster_host.call_args)
        self.assertEqual('broadcaster host name',
                         actual_configuration['broadcaster-host'])

        self.assertEqual(call(), mock_loader.get_broadcaster_port.call_args)
        self.assertEqual(12345, actual_configuration['broadcaster-port'])
