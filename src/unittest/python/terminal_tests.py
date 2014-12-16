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

from mockito import mock, verify

from yadt_controller.terminal import TeamCityProgressMessageHandler


class TeamcityMessageTest(unittest.TestCase):

    def test_should_output_teamcity_progress_messages(self):
        mock_stream = mock()

        progress_handler = TeamCityProgressMessageHandler()

        progress_handler.output_progress(mock_stream, 'service foo is now up')

        verify(mock_stream).write("##teamcity[progressMessage 'service foo is now up']\n")
