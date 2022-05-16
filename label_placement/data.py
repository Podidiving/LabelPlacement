from enum import Enum, auto
from dataclasses import dataclass


class Position(Enum):
    LEFT_MIDDLE = auto()
    TOP_MIDDLE = auto()
    RIGHT_MIDDLE = auto()
    BOTTOM_MIDDLE = auto()
    LEFT_TOP = auto()
    RIGHT_TOP = auto()
    RIGHT_BOTTOM = auto()
    LEFT_BOTTOM = auto()


@dataclass
class Label:
    x: float
    y: float
    width: float
    height: float
    position: Position


class Box:
    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)

        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)

    def get_width(self) -> float:
        return self.x2 - self.x1

    def get_height(self) -> float:
        return self.y2 - self.y1
