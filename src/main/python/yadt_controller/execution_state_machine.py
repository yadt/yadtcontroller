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
            {'name': 'finished', 'src': 'pending', 'dst': 'success'},
            {'name': 'started', 'src': 'pending', 'dst': 'pending'}
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
