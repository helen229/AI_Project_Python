from CardSegment import CardSegment
from CardSegment import Color
from CardSegment import Dot


class Card:
    max_x = 8
    max_y = 12
    card_id = 0

    def __init__(self, px, py, card_type, owner):

        self.card_type = card_type
        self.owner = owner
        # adjust indexes
        x = ord(px) - 65
        y = py - 1

        # set attributes for two sides
        if card_type <= 4:
            # side 1, red bg and solid dot
            anchor_color = Color.RED
            anchor_dot = Dot.SOLID
            rotating_color = Color.WHITE
            rotating_dot = Dot.EMPTY
        else:
            # side 2, red bg and empty dot
            anchor_color = Color.RED
            anchor_dot = Dot.EMPTY
            rotating_color = Color.WHITE
            rotating_dot = Dot.SOLID
        self.seg = [None, None]
        tmp_card_type = card_type % 4
        if tmp_card_type == 1:
            self.seg[0] = CardSegment(anchor_color, anchor_dot, self.card_id, x, y, owner)
            self.seg[1] = CardSegment(rotating_color, rotating_dot, self.card_id, x + 1, y, owner)
        elif tmp_card_type == 2:
            self.seg[0] = CardSegment(rotating_color, rotating_dot, self.card_id, x, y, owner)
            self.seg[1] = CardSegment(anchor_color, anchor_dot, self.card_id, x, y + 1, owner)
        elif tmp_card_type == 3:
            self.seg[0] = CardSegment(rotating_color, rotating_dot, self.card_id, x, y, owner)
            self.seg[1] = CardSegment(anchor_color, anchor_dot, self.card_id, x + 1, y, owner)
        else:
            self.seg[0] = CardSegment(anchor_color, anchor_dot, self.card_id, x, y, owner)
            self.seg[1] = CardSegment(rotating_color, rotating_dot, self.card_id, x, y + 1, owner)

        self.card_id += 1

    def __eq__(self, other):
        return self.seg[0] == other.seg[0] and self.seg[1] == other.seg[1]

    def __repr__(self):
        return '(ID:{!r}, T:{!r}, O:{!r})'.format(self.card_id, self.card_type, self.owner)

    def is_valid(self):
        # validate if the rotating segment is out of board
        if 0 <= self.seg[1].x < self.max_x and 0 <= self.seg[1].y < self.max_y:
            return True
        else:
            return False
