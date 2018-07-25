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

class KeyEvent(Event):
    TYPE = "KeyEvent"
    def __init__(self, key):
        super(KeyEvent, self).__init__(self.TYPE, key)

class KeyDownEvent(Event):
    TYPE = "KeyDownEvent"
    def __init__(self, key):
        super(KeyDownEvent, self).__init__(self.TYPE, key)

class KeyUpEvent(Event):
    TYPE = "KeyUpEvent"
    def __init__(self, key):
        super(KeyUpEvent, self).__init__(self.TYPE, key)

class InputDownEvent(object):
    TYPE = "InputDown"

class TestEvent(Event):
    TYPE = "Test"
    def __init__(self, data):
        super(TestEvent, self).__init__(self.TYPE, data)
