from enum import Enum, auto


class Direction(Enum):
    STOP = auto()
    FORWARD = auto()
    LEFT = auto()
    RIGHT = auto()
    BACKWARD = auto()  # おそらく未使用
