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
    ONE = Event(TYPE, 'ONE')


class TestEvent(object):
    TYPE = "Test"
    RIGHT = Event(TYPE,'RIGHT')
