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

from mock import Mock, call, patch

from yadt_controller.configuration import (DEFAULT_BROADCASTER_HOST,
                                        DEFAULT_BROADCASTER_PORT,
                                        SECTION_BROADCASTER,
                                        ConfigurationException,
                                        ReceiverConfigLoader,
                                        YadtConfigParser,
                                        load)


class YadtConfigParserTests (unittest.TestCase):
    def test_should_create_instance_of_YadtConfigParser (self):
        parser = YadtConfigParser()

        name_of_type = parser._parser.__class__.__name__
        self.assertEqual('SafeConfigParser', name_of_type)


    @patch('yadtreceiver.configuration.sys')
    @patch('yadtreceiver.configuration.os.path.exists')
    @patch('__builtin__.exit')
    def test_should_exit_when_configuration_file_does_not_exist (self, mock_exit, mock_exists, mock_log):
        mock_parser = Mock(YadtConfigParser)
        mock_exists.return_value = False

        YadtConfigParser.read_configuration_file(mock_parser, 'some.cfg')

        self.assertEqual(call('some.cfg'), mock_exists.call_args)
        self.assertEqual(call(1), mock_exit.call_args)


    @patch('yadtreceiver.configuration.sys')
    @patch('yadtreceiver.configuration.os.path.exists')
    def test_should_read_configuration_file (self, mock_exists, mock_log):
        mock_parser = Mock(YadtConfigParser)
        mock_wrapped_parser = Mock()
        mock_parser._parser = mock_wrapped_parser
        mock_exists.return_value = True

        YadtConfigParser.read_configuration_file(mock_parser, 'some.cfg')

        self.assertEqual(call(['some.cfg']), mock_wrapped_parser.read.call_args)


    def test_should_raise_exception_when_given_option_is_not_digit (self):
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = 'abcdef'

        self.assertRaises(ConfigurationException, YadtConfigParser.get_option_as_int, mock_parser, 'section', 'option', 'default_value')


    def test_should_return_default_when_option_not_available (self):
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = ''

        actual_option = YadtConfigParser.get_option_as_list(mock_parser, 'section', 'option', 'default_value')

        self.assertEqual('default_value', actual_option)
        self.assertEqual(call('section', 'option', ''), mock_parser.get_option.call_args)


    def test_should_return_list_separated_by_comma (self):
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = ' abc, def,ghi,jkl   '

        actual_option = YadtConfigParser.get_option_as_list(mock_parser, 'section', 'option', 'default_value')

        self.assertEqual(['abc', 'def', 'ghi', 'jkl'], actual_option)
        self.assertEqual(call('section', 'option', ''), mock_parser.get_option.call_args)


    def test_should_return_a_set (self):
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option_as_list.return_value = ['abc', 'def', 'ghi', 'jkl']

        actual_option = YadtConfigParser.get_option_as_set(mock_parser, 'section', 'option', 'default_value')

        self.assertEqual(set(['abc', 'def', 'ghi', 'jkl']), actual_option)
        self.assertEqual(call('section', 'option', 'default_value'), mock_parser.get_option_as_list.call_args)


    def test_should_return_yes_as_boolean_value_true (self):
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = 'yes'

        actual_option = YadtConfigParser.get_option_as_yes_or_no_boolean(mock_parser, 'section', 'option', 'default_value')

        self.assertEqual(True, actual_option)
        self.assertEqual(call('section', 'option', 'default_value'), mock_parser.get_option.call_args)


    def test_should_return_no_as_boolean_value_false (self):
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = 'no'

        actual_option = YadtConfigParser.get_option_as_yes_or_no_boolean(mock_parser, 'section', 'option', 'default_value')

        self.assertEqual(False, actual_option)
        self.assertEqual(call('section', 'option', 'default_value'), mock_parser.get_option.call_args)


    def test_should_raise_exception_when_given_value_is_not_yes_or_no (self):
        mock_parser = Mock(YadtConfigParser)
        mock_wrapped_parser = Mock()
        mock_wrapped_parser.get_option.return_value = 'tralala'
        mock_parser._parser = mock_wrapped_parser

        self.assertRaises(ConfigurationException, YadtConfigParser.get_option_as_yes_or_no_boolean, mock_parser, 'section', 'option', 'default_value')


    def test_should_return_option_from_section (self):
        mock_parser = Mock(YadtConfigParser)
        mock_wrapped_parser = Mock()
        mock_wrapped_parser.has_section.return_value = True
        mock_wrapped_parser.has_option.return_value = True
        mock_wrapped_parser.get.return_value = 'the option'
        mock_parser._parser = mock_wrapped_parser

        actual_option = YadtConfigParser.get_option(mock_parser, 'section', 'option', 'default_value')

        self.assertEqual('the option', actual_option)
        self.assertEqual(call('section', 'option'), mock_wrapped_parser.has_option.call_args)
        self.assertEqual(call('section', 'option'), mock_wrapped_parser.get.call_args)


    def test_should_return_default_value_when_option_not_in_section (self):
        mock_parser = Mock(YadtConfigParser)
        mock_wrapped_parser = Mock()
        mock_wrapped_parser.has_section.return_value = True
        mock_wrapped_parser.has_option.return_value = False
        mock_parser._parser = mock_wrapped_parser

        actual_option = YadtConfigParser.get_option(mock_parser, 'section', 'option', 'default_value')

        self.assertEqual('default_value', actual_option)
        self.assertEqual(call('section', 'option'), mock_wrapped_parser.has_option.call_args)


    def test_should_return_option_as_int (self):
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = '123456'

        actual_option = YadtConfigParser.get_option_as_int(mock_parser, 'section', 'option', 'default_value')

        self.assertEqual(123456, actual_option)
        self.assertEqual(call('section', 'option', 'default_value'), mock_parser.get_option.call_args)


class ReceiverConfigLoaderTests (unittest.TestCase):
    def test_should_create_instance_of_SafeConfigParser (self):
        parser = ReceiverConfigLoader()

        name_of_type = parser._parser.__class__.__name__
        self.assertEqual('YadtConfigParser', name_of_type)


    def test_should_return_broadcaster_host_option (self):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = 'broadcaster.host'
        mock_loader._parser = mock_parser

        actual_broadcaster_host = ReceiverConfigLoader.get_broadcaster_host(mock_loader)

        self.assertEqual('broadcaster.host', actual_broadcaster_host)
        self.assertEqual(call(SECTION_BROADCASTER, 'host', DEFAULT_BROADCASTER_HOST), mock_parser.get_option.call_args)


    def test_should_return_broadcaster_port_option (self):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option_as_int.return_value = 8081
        mock_loader._parser = mock_parser

        actual_broadcaster_port = ReceiverConfigLoader.get_broadcaster_port(mock_loader)

        self.assertEqual(8081, actual_broadcaster_port)
        self.assertEqual(call(SECTION_BROADCASTER, 'port', DEFAULT_BROADCASTER_PORT), mock_parser.get_option_as_int.call_args)


    def test_should_return_graphite_active (self):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option_as_yes_or_no_boolean.return_value = True
        mock_loader._parser = mock_parser

        actual_graphite_active = ReceiverConfigLoader.get_graphite_active(mock_loader)

        self.assertEqual(True, actual_graphite_active)
        self.assertEqual(call(SECTION_GRAPHITE, 'active', DEFAULT_GRAPHITE_ACTIVE), mock_parser.get_option_as_yes_or_no_boolean.call_args)


    def test_should_return_graphite_host (self):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = 'graphite.host'
        mock_loader._parser = mock_parser

        actual_graphite_host = ReceiverConfigLoader.get_graphite_host(mock_loader)

        self.assertEqual('graphite.host', actual_graphite_host)
        self.assertEqual(call(SECTION_GRAPHITE, 'host', DEFAULT_GRAPHITE_HOST), mock_parser.get_option.call_args)


    def test_should_return_graphite_port (self):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option_as_int.return_value = 2003
        mock_loader._parser = mock_parser

        actual_graphite_port = ReceiverConfigLoader.get_graphite_port(mock_loader)

        self.assertEqual(2003, actual_graphite_port)
        self.assertEqual(call(SECTION_GRAPHITE, 'port', DEFAULT_GRAPHITE_PORT), mock_parser.get_option_as_int.call_args)


    @patch('yadtreceiver.configuration.socket')
    def test_should_return_hostname_from_receiver_section (self, mock_socket):
        mock_socket.gethostname.return_value = 'localhost'

        mock_loader = Mock(ReceiverConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = 'actual.hostname'
        mock_loader._parser = mock_parser

        actual_hostname = ReceiverConfigLoader.get_hostname(mock_loader)

        self.assertEqual('actual.hostname', actual_hostname)
        self.assertEqual(call(), mock_socket.gethostname)
        self.assertEqual(call(SECTION_RECEIVER, 'hostname', 'localhost'), mock_parser.get_option.call_args)


    def test_should_return_log_filename (self):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = 'filename.log'
        mock_loader._parser = mock_parser

        actual_log_filename = ReceiverConfigLoader.get_log_filename(mock_loader)

        self.assertEqual('filename.log', actual_log_filename)
        self.assertEqual(call(SECTION_RECEIVER, 'log_filename', DEFAULT_LOG_FILENAME), mock_parser.get_option.call_args)


    def test_should_return_python_command (self):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = '/spam/eggs/python'
        mock_loader._parser = mock_parser

        actual_python_command = ReceiverConfigLoader.get_python_command(mock_loader)

        self.assertEqual('/spam/eggs/python', actual_python_command)
        self.assertEqual(call(SECTION_RECEIVER, 'python_command', DEFAULT_PYTHON_COMMAND), mock_parser.get_option.call_args)


    def test_should_return_script_to_execute (self):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = '/script/to/execute'
        mock_loader._parser = mock_parser

        actual_script_to_execute = ReceiverConfigLoader.get_script_to_execute(mock_loader)

        self.assertEqual('/script/to/execute', actual_script_to_execute)
        self.assertEqual(call(SECTION_RECEIVER, 'script_to_execute', DEFAULT_SCRIPT_TO_EXECUTE), mock_parser.get_option.call_args)


    def test_should_return_targets (self):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option_as_set.return_value = set(['abc', 'def'])
        mock_loader._parser = mock_parser

        actual_targets = ReceiverConfigLoader.get_targets(mock_loader)

        self.assertEqual(set(['abc', 'def']), actual_targets)
        self.assertEqual(call(SECTION_RECEIVER, 'targets', DEFAULT_TARGETS), mock_parser.get_option_as_set.call_args)


    def test_should_return_targets_directory (self):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.get_option.return_value = '/directory/with/targets'
        mock_loader._parser = mock_parser

        actual_targets_directory = ReceiverConfigLoader.get_targets_directory(mock_loader)

        self.assertEqual('/directory/with/targets', actual_targets_directory)
        self.assertEqual(call(SECTION_RECEIVER, 'targets_directory', DEFAULT_TARGETS_DIRECTORY), mock_parser.get_option.call_args)


    def test_should_delegate_read_configuration_file (self):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_parser = Mock(YadtConfigParser)
        mock_parser.read_configuration_file.return_value = {'spam': 'eggs'}
        mock_loader._parser = mock_parser

        actual_configuration = ReceiverConfigLoader.read_configuration_file(mock_loader, 'filename.cfg')

        self.assertEqual({'spam': 'eggs'}, actual_configuration)
        self.assertEqual(call('filename.cfg'), mock_parser.read_configuration_file.call_args)


class LoadTest (unittest.TestCase):
    @patch('yadtreceiver.configuration.ReceiverConfigLoader')
    def test_should_load_configuration_from_file (self, mock_loader_class):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_loader_class.return_value = mock_loader

        actual_configuration = load('abc')

        self.assertEqual(call('abc'), mock_loader.read_configuration_file.call_args)


    @patch('yadtreceiver.configuration.ReceiverConfigLoader')
    def test_should_get_broadcaster_properties_from_parser (self, mock_loader_class):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_loader.get_broadcaster_host.return_value = 'broadcaster host'
        mock_loader.get_broadcaster_port.return_value = 12345
        mock_loader_class.return_value = mock_loader

        actual_configuration = load('abc')

        self.assertEqual(call(), mock_loader.get_broadcaster_host.call_args)
        self.assertEqual('broadcaster host', actual_configuration['broadcaster_host'])

        self.assertEqual(call(), mock_loader.get_broadcaster_port.call_args)
        self.assertEqual(12345, actual_configuration['broadcaster_port'])


    @patch('yadtreceiver.configuration.ReceiverConfigLoader')
    def test_should_get_graphite_properties_from_parser (self, mock_loader_class):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_loader.get_graphite_active.return_value = True
        mock_loader.get_graphite_host.return_value = 'graphite host'
        mock_loader.get_graphite_port.return_value = 54321
        mock_loader_class.return_value = mock_loader

        actual_configuration = load('abc')

        self.assertEqual(call(), mock_loader.get_graphite_active.call_args)
        self.assertEqual(True, actual_configuration['graphite_active'])

        self.assertEqual(call(), mock_loader.get_graphite_host.call_args)
        self.assertEqual('graphite host', actual_configuration['graphite_host'])

        self.assertEqual(call(), mock_loader.get_graphite_port.call_args)
        self.assertEqual(54321, actual_configuration['graphite_port'])


    @patch('yadtreceiver.configuration.ReceiverConfigLoader')
    def test_should_get_receiver_properties_from_parser (self, mock_loader_class):
        mock_loader = Mock(ReceiverConfigLoader)
        mock_loader.get_hostname.return_value = 'this is a name'
        mock_loader.get_log_filename.return_value = '/var/log/somewhere/rec.log'
        mock_loader.get_python_command.return_value = '/usr/bin/python'
        mock_loader.get_script_to_execute.return_value = '/usr/bin/yadtshell'
        mock_loader.get_log_filename.return_value = '/var/log/somewhere/rec.log'
        mock_loader.get_targets.return_value = set(['dev123'])
        mock_loader.get_targets_directory.return_value = '/etc/yadtshell/targets'
        mock_loader_class.return_value = mock_loader

        actual_configuration = load('abc')

        self.assertEqual(call(), mock_loader.get_hostname.call_args)
        self.assertEqual('this is a name', actual_configuration['hostname'])

        self.assertEqual(call(), mock_loader.get_log_filename.call_args)
        self.assertEqual('/var/log/somewhere/rec.log', actual_configuration['log_filename'])

        self.assertEqual(call(), mock_loader.get_python_command.call_args)
        self.assertEqual('/usr/bin/python', actual_configuration['python_command'])

        self.assertEqual(call(), mock_loader.get_script_to_execute.call_args)
        self.assertEqual('/usr/bin/yadtshell', actual_configuration['script_to_execute'])

        self.assertEqual(call(), mock_loader.get_targets.call_args)
        self.assertEqual(set(['dev123']), actual_configuration['targets'])

        self.assertEqual(call(), mock_loader.get_targets_directory.call_args)
        self.assertEqual('/etc/yadtshell/targets', actual_configuration['targets_directory'])