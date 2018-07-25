from ..common.event import Event

class CameraResultEvent(Event):
    TYPE = "CameraResultEvent"
    P1 = "P1"
    P2 = "P2"
    def __init__(self, result_type, data):
        super(CameraResultEvent, self).__init__(self.TYPE, (result_type, data))

class YImageEvent(Event):
    TYPE = "YImage"
    def __init__(self, data):
        super(YImageEvent, self).__init__(self.TYPE, data)

class LatencyEvent(Event):
    TYPE = "LatencyEvent"
    P1_PROCESSING = "P1Processing"
    P2_PROCESSING = "P2Processing"
    def __init__(self, latency_type, time):
        super(LatencyEvent, self).__init__(self.TYPE, (latency_type, time))

class Key(object):
    ESCAPE = 'ESCAPE'
    Q = 'Q'
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    ENTER = 'ENTER'
    W = 'W'
    A = 'A'
    S = 'S'
    D = 'D'
    I = 'I'
    J = 'J'
    K = 'K'
    L = 'L'
    NUM_1 = '1'

class KeyDownEvent(Event):
    TYPE = "KeyDownEvent"
    def __init__(self, key):
        super(KeyDownEvent, self).__init__(self.TYPE, key)

class KeyUpEvent(Event):
    TYPE = "KeyUpEvent"
    def __init__(self, key):
        super(KeyUpEvent, self).__init__(self.TYPE, key)

class InputEvent(object):
    TYPE = "Input"
    ESCAPE = Event(TYPE, 'ESCAPE')
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

class InputDownEvent(object):
    TYPE = "InputDown"

class TestEvent(Event):
    TYPE = "Test"
    def __init__(self, data):
        super(TestEvent, self).__init__(self.TYPE, data)
