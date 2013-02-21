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
from docopt import docopt

from mockito import when, verify, unstub, any as any_value, mock

import yadt_controller


class YadtControllerTests(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_should_write_name_and_version_to_stdout_and_exit(self):
        when(yadt_controller).write(any_value()).thenReturn(None)
        when(yadt_controller).docopt(any_value()).thenReturn({})
        when(yadt_controller.sys).exit(any_value).thenReturn(None)

        yadt_controller.print_name_and_version_and_exit()

        verify(yadt_controller).write('yadtcontroller ${version}')
        verify(yadt_controller.sys).exit(0)

    def test_should_parse_command_line_using_docopt_with_program_version_when_run(self):
        when(yadt_controller).write(any_value()).thenReturn(None)
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({})

        yadt_controller.run()

        verify(yadt_controller).docopt(yadt_controller.__doc__, version='${version}')

    def test_should_print_name_and_version_when_version_option_was_found(self):
        mock_arguments = {'--version': True}
        when(yadt_controller).print_name_and_version_and_exit().thenReturn(None)
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn(mock_arguments)

        yadt_controller.run()

        verify(yadt_controller).print_name_and_version_and_exit()

    def test_show_version_option_was_given_should_return_true_when_option_is_given(self):
        arguments = {'--version': True}
        self.assertTrue(yadt_controller._show_version_option_was_given(arguments))

    def test_show_version_option_was_given_should_return_false_when_option_is_not_given_or_none(self):
        arguments = {'--version': False}
        self.assertFalse(yadt_controller._show_version_option_was_given(arguments))


        arguments = {'--version': None}
        self.assertFalse(yadt_controller._show_version_option_was_given(arguments))

    def test_show_version_option_was_given_should_return_false_when_option_is_not_present(self):
        arguments = {}
        self.assertFalse(yadt_controller._show_version_option_was_given(arguments))
