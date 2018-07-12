from ..common.event import Event

class YImageEvent():
    TYPE = "YImage"

class DrawEvent():
    TYPE = "Draw"

class InputEvent():
    TYPE = "Input"
    ESCAPE = Event(TYPE,'ESCAPE')
    Q = Event(TYPE, 'Q')
    UP = Event(TYPE,'UP')
    DOWN = Event(TYPE,'DOWN')
    LEFT = Event(TYPE,'LEFT')

class TestEvent():
    TYPE = "Test"
    RIGHT = Event(TYPE,'RIGHT')
