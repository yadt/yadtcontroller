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

"""
        Provides convenience functions for tracking the remote execution of a
        program.
"""

import getpass
import socket
from datetime import datetime


def generate_tracking_id(target):
    user_name = getpass.getuser()
    user_host_name = socket.getfqdn()
    timestamp = get_timestamp()
    return '"({0}):{1}@{2}->{3}"'.format(timestamp, user_name, user_host_name, target)


# datetime.so cannot be monkey-patched, so isolate it instead
def get_timestamp():  # pragma: no cover
    return str(datetime.now())
