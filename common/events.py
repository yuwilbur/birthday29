from event import Event

class DrawEvent():
    TYPE = __name__

class InputEvent():
    TYPE = __name__
    ESCAPE = Event(TYPE,'ESCAPE')
    Q = Event(TYPE, 'Q')
    UP = Event(TYPE,'UP')
    DOWN = Event(TYPE,'DOWN')
    LEFT = Event(TYPE,'LEFT')
    RIGHT = Event(TYPE,'RIGHT')
