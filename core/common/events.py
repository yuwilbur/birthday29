from ..common.event import Event

class YImageEvent(Event):
    TYPE = "YImage"
    def __init__(self, data):
        super(YImageEvent, self).__init__(self.TYPE, data)

class GrayscaleImageEvent(Event):
    TYPE = "GrayscaleImage"
    def __init__(self, data):
        super(GrayscaleImageEvent, self).__init__(self.TYPE, data)

class InputEvent(object):
    TYPE = "Input"
    ESCAPE = Event(TYPE,'ESCAPE')
    Q = Event(TYPE, 'Q')
    UP = Event(TYPE,'UP')
    DOWN = Event(TYPE,'DOWN')
    LEFT = Event(TYPE,'LEFT')
    RIGHT = Event(TYPE, 'RIGHT')
    ENTER = Event(TYPE, 'ENTER')
    W = Event(TYPE, 'W')
    A = Event(TYPE, 'A')
    S = Event(TYPE, 'S')
    D = Event(TYPE, 'D')
    I = Event(TYPE, 'I')
    J = Event(TYPE, 'J')
    K = Event(TYPE, 'K')
    L = Event(TYPE, 'L')
    ONE = Event(TYPE, '1')

class TestEvent(Event):
    TYPE = "Test"
    def __init__(self, data):
        super(TestEvent, self).__init__(self.TYPE, data)
