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

from requests import get, codes
import logging

logger = logging.getLogger("rest_api")
logging.getLogger("requests").setLevel(logging.ERROR)


class EndpointException(BaseException):
    pass


class TargetInfoEndpoint(object):

    def __init__(self, target, host, port):
        self.target = target
        self.host = host
        self.port = port

    def fetch(self, timeout_in_seconds=5):
        info_url = "http://{0}:{1}/api/v1/targets/{2}/full".format(self.host,
                                                                   self.port,
                                                                   self.target)
        logger.debug("Fetching info from {0}".format(info_url))

        try:
            response = get(info_url, timeout=timeout_in_seconds)
        except Exception as e:
            raise EndpointException(e)

        self.validate_response(response)

        return response.text

    def validate_response(self, response):
        if response.status_code != codes.ok:
            raise EndpointException(
                "Info request returned non-ok code {0} ({1})".format(response.status_code,
                                                                     response.reason))
