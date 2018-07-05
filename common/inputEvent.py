from event import Event

class InputEvent():
    TYPE = 'InputEvent'
    ESCAPE = Event(TYPE,'ESCAPE')
    UP = Event(TYPE,'UP')
    DOWN = Event(TYPE,'DOWN')
    LEFT = Event(TYPE,'LEFT')
    RIGHT = Event(TYPE,'RIGHT')
