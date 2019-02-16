import unittest
from Card import Card
from CardSegment import CardSegment
from CardSegment import Color
from CardSegment import Dot


class TestCard(unittest.TestCase):

    def test_card_type_side1(self):
        # type 1
        card = Card('A', 1, 1, 0)
        self.assertEqual(CardSegment(Color.RED, Dot.SOLID, 0, 0, 0, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.WHITE, Dot.EMPTY, 0, 1, 0, 1), card.seg[1])
        # type 1 out of bound
        card = Card('H', 1, 1, 0)
        self.assertEqual(CardSegment(Color.RED, Dot.SOLID, 0, 7, 0, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.WHITE, Dot.EMPTY, 0, 8, 0, 1), card.seg[1])
        self.assertFalse(card.is_valid())

        # type 2
        card = Card('A', 2, 2, 0)
        self.assertEqual(CardSegment(Color.RED, Dot.SOLID, 0, 0, 1, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.WHITE, Dot.EMPTY, 0, 0, 0, 1), card.seg[1])
        # type 2 out of bound
        card = Card('A', 1, 2, 0)
        self.assertEqual(CardSegment(Color.RED, Dot.SOLID, 0, 0, 0, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.WHITE, Dot.EMPTY, 0, 0, -1, 1), card.seg[1])
        self.assertFalse(card.is_valid())

        # type 3
        card = Card('A', 1, 3, 0)
        self.assertEqual(CardSegment(Color.WHITE, Dot.EMPTY, 0, 0, 0, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.RED, Dot.SOLID, 0, 1, 0, 1), card.seg[1])
        # type 2 out of bound
        card = Card('H', 1, 3, 0)
        self.assertEqual(CardSegment(Color.WHITE, Dot.EMPTY, 0, 7, 0, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.RED, Dot.SOLID, 0, 8, 0, 1), card.seg[1])
        self.assertFalse(card.is_valid())

        # type 4
        card = Card('A', 2, 4, 0)
        self.assertEqual(CardSegment(Color.WHITE, Dot.EMPTY, 0, 0, 1, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.RED, Dot.SOLID, 0, 0, 0, 1), card.seg[1])
        # type 4 out of bound
        card = Card('A', 1, 4, 0)
        self.assertEqual(CardSegment(Color.WHITE, Dot.EMPTY, 0, 0, 0, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.RED, Dot.SOLID, 0, 0, -1, 1), card.seg[1])
        self.assertFalse(card.is_valid())

    def test_card_type_side2(self):
        # type 5
        card = Card('A', 1, 5, 0)
        self.assertEqual(CardSegment(Color.RED, Dot.EMPTY, 0, 0, 0, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.WHITE, Dot.SOLID, 0, 1, 0, 1), card.seg[1])
        # type 5 out of bound
        card = Card('H', 1, 5, 0)
        self.assertEqual(CardSegment(Color.RED, Dot.EMPTY, 0, 7, 0, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.WHITE, Dot.SOLID, 0, 8, 0, 1), card.seg[1])
        self.assertFalse(card.is_valid())

        # type 6
        card = Card('A', 2, 6, 0)
        self.assertEqual(CardSegment(Color.RED, Dot.EMPTY, 0, 0, 1, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.WHITE, Dot.SOLID, 0, 0, 0, 1), card.seg[1])
        # type 6 out of bound
        card = Card('A', 1, 6, 0)
        self.assertEqual(CardSegment(Color.RED, Dot.EMPTY, 0, 0, 0, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.WHITE, Dot.SOLID, 0, 0, -1, 1), card.seg[1])
        self.assertFalse(card.is_valid())

        # type 7
        card = Card('A', 1, 7, 0)
        self.assertEqual(CardSegment(Color.WHITE, Dot.SOLID, 0, 0, 0, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.RED, Dot.EMPTY, 0, 1, 0, 1), card.seg[1])
        # type 7 out of bound
        card = Card('H', 1, 7, 0)
        self.assertEqual(CardSegment(Color.WHITE, Dot.SOLID, 0, 7, 0, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.RED, Dot.EMPTY, 0, 8, 0, 1), card.seg[1])
        self.assertFalse(card.is_valid())

        # type 8
        card = Card('A', 2, 8, 0)
        self.assertEqual(CardSegment(Color.WHITE, Dot.SOLID, 0, 0, 1, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.RED, Dot.EMPTY, 0, 0, 0, 1), card.seg[1])
        # type 8 out of bound
        card = Card('A', 1, 8, 0)
        self.assertEqual(CardSegment(Color.WHITE, Dot.SOLID, 0, 0, 0, 0), card.seg[0])
        self.assertEqual(CardSegment(Color.RED, Dot.EMPTY, 0, 0, -1, 1), card.seg[1])
        self.assertFalse(card.is_valid())
