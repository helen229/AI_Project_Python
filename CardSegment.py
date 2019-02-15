from enum import Enum


class Color(Enum):
    RED = 1
    WHITE = 2


class Dot(Enum):
    SOLID = 1
    EMPTY = 2


class CardSegment:

    def __init__(self, color, dot, parent_id, px, py):
        self.color = color
        self.dot = dot
        self.parent_id = parent_id
        self.px = px
        self.py = py

    def set_position(self, px, py):
        self.px = px
        self.py = py

    def __eq__(self, other):
        return self.color == other.color and self.dot == other.dot and self.px == other.px and self.py == other.py

    def __repr__(self):
        return '{}({!r}, {!r}, {!r}, {!r})'.format(
            self.__class__.__name__,
            self.color, self.dot, self.px, self.py)

# p1 = Card("W", "A","1",1)
#
# print(p1.x)
# print(p1.y)
# class Person:
#   def __init__(mysillyobject, name, age):
#     mysillyobject.name = name
#     mysillyobject.age = age
#
#   def myfunc(abc):
#     print("Hello my name is " + abc.name)
#
# p1 = Person("John", 36)
# p1.myfunc()
