from enum import Enum, auto


class State(Enum):
    """プログラムの状態
    """
    ERROR = auto()
    EXIT = auto()
    NORMAL = auto()
