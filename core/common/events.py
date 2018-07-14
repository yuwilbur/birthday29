from ..common.event import Event

class YImageEvent(object):
    TYPE = "YImage"

class RGBImageEvent(object):
    TYPE = "RGBImage"

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


class TestEvent(object):
    TYPE = "Test"
    RIGHT = Event(TYPE,'RIGHT')
