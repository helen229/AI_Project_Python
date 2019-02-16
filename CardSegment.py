from enum import Enum


class Color(Enum):
    RED = 1
    WHITE = 2


class Dot(Enum):
    SOLID = 1
    EMPTY = 2


class CardSegment:

    def __init__(self, color, dot, parent, x, y, owner):
        self.color = color
        self.dot = dot
        self.parent = parent
        self.x = x
        self.y = y
        self.owner = owner

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.color == other.color and self.dot == other.dot and self.x == other.x and self.y == other.y

    def __repr__(self):
        return '(ID:{!r},{!r},{!r},{!r},{!r},{!r})'.format(self.parent.card_id, self.color, self.dot, self.x, self.y, self.owner)

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
