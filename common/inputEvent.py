from event import Event

class InputEvent():
    TYPE = 'InputEvent'
    ESCAPE = Event(TYPE,'ESCAPE')
    Q = Event(TYPE, 'Q')
    UP = Event(TYPE,'UP')
    DOWN = Event(TYPE,'DOWN')
    LEFT = Event(TYPE,'LEFT')
    RIGHT = Event(TYPE,'RIGHT')
