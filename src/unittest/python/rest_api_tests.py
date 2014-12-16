#   yadtcontroller
#   Copyright (C) 2014 Immobilien Scout GmbH
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

from mock import patch, Mock

from unittest import TestCase

from yadt_controller.rest_api import (EndpointException, TargetInfoEndpoint)


class Test(TestCase):

    def setUp(self):
        self.logging_patcher = patch("yadt_controller.rest_api.logger")
        self.logging_patcher.start()

        self.endpoint = TargetInfoEndpoint("any-target", "any-host", 8080)

    def tearDown(self):
        self.logging_patcher.stop()

    def test_validation_should_do_nothing_when_response_is_valid(self):
        self.endpoint.validate_response(Mock(status_code=200, reason="OK"))

    def test_validation_should_raise_when_response_is_invalid(self):
        self.assertRaises(EndpointException,
                          self.endpoint.validate_response, Mock(status_code=400, reason="bad request"))

    @patch("yadt_controller.rest_api.get")
    def test_should_fetch_info_and_return_it_with_default_timeout(self, get):
        get.return_value = Mock(text="this is the body of the get response", status_code=200)

        actual_info = self.endpoint.fetch()

        self.assertEqual(actual_info, "this is the body of the get response")

    @patch("yadt_controller.rest_api.get")
    def test_should_call_specified_url_with_default_timeout(self, get):
        get.return_value = Mock(status_code=200)

        actual_info = self.endpoint.fetch()

        get.assert_called_with('http://any-host:8080/api/v1/targets/any-target/full', timeout=5)

    @patch("yadt_controller.rest_api.get")
    def test_should_call_specified_url_with_userset_timeout(self, get):
        get.return_value = Mock(status_code=200)

        actual_info = self.endpoint.fetch(42)

        get.assert_called_with('http://any-host:8080/api/v1/targets/any-target/full', timeout=42)
