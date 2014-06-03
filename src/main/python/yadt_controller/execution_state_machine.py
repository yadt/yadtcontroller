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
        The state machine that describes the protocol followed by the YADT
        controller. The events received from a YADT broadcaster alter the initial
        state until it is finished or errored.
"""
from fysom import Fysom


def create_execution_state_machine_with_callbacks(waiting_callback,
                                                  failed_callback,
                                                  pending_callback,
                                                  success_callback,
                                                  failure_callback,
                                                  waiting_timeout_callback,
                                                  pending_timeout_callback):

    fsm = Fysom({
        'initial': 'idle',
        'events': [
            {'name': 'finished', 'src': 'idle', 'dst': 'success'},
            {'name': 'waiting_timeout', 'src': 'idle', 'dst': 'failure'},
            {'name': 'request', 'src': 'idle', 'dst': 'waiting'},
            {'name': 'waiting_timeout', 'src': 'waiting', 'dst': 'failure'},
            {'name': 'waiting_timeout', 'src': 'pending', 'dst': 'pending'},
            {'name': 'failed', 'src': 'waiting', 'dst': 'waiting'},
            {'name': 'started', 'src': 'waiting', 'dst': 'pending'},
            {'name': 'pending_timeout', 'src': 'pending', 'dst': 'failure'},
            {'name': 'failed', 'src': 'pending', 'dst': 'failure'},
            {'name': 'failed', 'src': 'failure', 'dst': 'failure'},
            {'name': 'finished', 'src': 'pending', 'dst': 'success'},
            {'name': 'finished', 'src': 'success', 'dst': 'success'},
            {'name': 'started', 'src': 'pending', 'dst': 'pending'},
            {'name': 'waiting_timeout', 'src': 'failure', 'dst': 'failure'},
            {'name': 'request', 'src': 'failure', 'dst': 'failure'}
        ],
        'callbacks': {
            'onwaiting': waiting_callback,
            'onfailed': failed_callback,
            'onpending': pending_callback,
            'onsuccess': success_callback,
            'onfailure': failure_callback,
            'onwaiting_timeout': waiting_timeout_callback,
            'onpending_timeout': pending_timeout_callback
        }
    })
    return fsm
