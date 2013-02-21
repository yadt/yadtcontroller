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

    def test_should_write_name_and_version_to_stdout(self):
        when(yadt_controller).write(any_value()).thenReturn(None)
        when(yadt_controller).docopt(any_value()).thenReturn({})

        yadt_controller.print_name_and_version_and_exit()

        verify(yadt_controller).write('yadtcontroller ${version}')

    def test_should_parse_command_line_using_docopt_with_program_version_when_run(self):
        when(yadt_controller).write(any_value()).thenReturn(None)
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn({})

        yadt_controller.run()

        verify(yadt_controller).docopt(any_value(), version='${version}')

    def test_should_print_name_and_version_when_version_option_was_found(self):
        mock_arguments = {'--version': True}
        when(yadt_controller).print_name_and_version_and_exit().thenReturn(None)
        when(yadt_controller).docopt(any_value(), version=any_value()).thenReturn(mock_arguments)

        yadt_controller.run()

        verify(yadt_controller).print_name_and_version_and_exit()