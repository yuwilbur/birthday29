from ..common.singleton import Singleton

class Event(object):
    def __init__(self, event_type, data=None):
        self._type = event_type
        self._data = data

    def __eq__(self, other):
        return self.type() == other.type() and self.data() == other.data()

    def type(self):
        return self._type

    def data(self):
        return self._data

class EventDispatcher(object):
    __metaclass__ = Singleton

    def __init__(self):
        self._events = dict()

    def __del__(self):
        self._events = None

    def has_listener(self, event_type, listener):
        if event_type in self._events.keys():
            return listener in self._events[event_type]
        else:
            return False

    def add_event_listener(self, event_type, listener):
        if not self.has_listener(event_type, listener):
            if not event_type in self._events.keys():
                self._events[event_type] = []
            self._events[event_type].append(listener)

    def remove_event_listener(self, event_type, listener):
        if self.has_listener(event_type, listener):
            self._events[event_type].remove(listener)
            if len(self._events[event_type]) == 0:
                del self._events[event_type]

    def dispatch_event(self, event):
        if event.type() in self._events.keys():
            for listener in self._events[event.type()]:
                listener(event)

