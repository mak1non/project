from enum import Enum, auto


class Direction(Enum):
    """進行方向
    """
    BACKWARD = auto()
    FORWARD = auto()
    LEFT = auto()
    RIGHT = auto()
    STOP = auto()
