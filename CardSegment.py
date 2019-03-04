from enum import Enum


class Color(Enum):
    RED = 1
    WHITE = 2


class Dot(Enum):
    SOLID = 1
    EMPTY = 2


class CardSegment:

    def __init__(self, color, dot, parent, x, y):
        self.color = color
        self.dot = dot
        self.parent = parent
        self.x = x
        self.y = y

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.color == other.color and self.dot == other.dot and self.x == other.x and self.y == other.y

    def __repr__(self):
        return '(ID:{!r},{!r},{!r},x:{!r},y:{!r})'.format(self.parent.card_id, self.color.name, self.dot.name, self.x, self.y)


