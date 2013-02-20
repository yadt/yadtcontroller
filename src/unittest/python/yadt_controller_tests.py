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
from mockito import when, verify, unstub, any as any_value

import yadt_controller

class YadtControllerTests(unittest.TestCase):
    def test_should_write_name_and_version_to_stdout(self):
        when(yadt_controller).write(any_value()).thenReturn(None)

        yadt_controller.run()

        verify(yadt_controller).write('yadtcontroller ${version}')
