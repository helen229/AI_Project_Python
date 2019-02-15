from CardSegment import CardSegment
from CardSegment import Color
from CardSegment import Dot


class Card:
    max_x = 8
    max_y = 12

    def __init__(self, card_id, px, py, card_type):

        self.card_type = card_type
        # adjust indexes
        px = ord(px) - 65
        py -= 1
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

        tmp_card_type = card_type % 4
        if tmp_card_type == 1:
            self.seg1 = CardSegment(anchor_color, anchor_dot, card_id, px, py)
            self.seg2 = CardSegment(rotating_color, rotating_dot, card_id, px + 1, py)
        elif tmp_card_type == 2:
            self.seg1 = CardSegment(anchor_color, anchor_dot, card_id, px, py)
            self.seg2 = CardSegment(rotating_color, rotating_dot, card_id, px, py - 1)
        elif tmp_card_type == 3:
            self.seg1 = CardSegment(rotating_color, rotating_dot, card_id, px, py)
            self.seg2 = CardSegment(anchor_color, anchor_dot, card_id, px + 1, py)
        else:
            self.seg1 = CardSegment(rotating_color, rotating_dot, card_id, px, py)
            self.seg2 = CardSegment(anchor_color, anchor_dot, card_id, px, py - 1)

    def __eq__(self, other):
        return self.seg1 == other.seg1 and self.seg2 == other.seg2

    def is_valid(self):
        # validate if the rotating segment is out of board
        if 0 <= self.seg2.px < self.max_x and 0 <= self.seg2.py < self.max_y:
            return True
        else:
            return False
