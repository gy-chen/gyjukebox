import collections


class EventEmitter:
    def __init__(self):
        self._listeners = collections.defaultdict(list)

    def on(self, event, callback):
        self._listeners[event].append(callback)

    def emit(self, event, *event_args):
        for callback in self._listeners[event]:
            callback(*event_args)
