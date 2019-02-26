"""
Game class
"""

import numpy as np
from enum import Enum
from Card import Card
from CardSegment import CardSegment
from CardSegment import Color
from CardSegment import Dot
from colorama import init
from colorama import Fore, Back, Style


class Phase(Enum):
    NORMAL = 1
    RECYCLE = 2


class Choice(Enum):
    COLOR = 1
    DOT = 2


class Game:
    max_x = 8
    max_y = 12

    init(autoreset=True)

    def __init__(self, choice_p1):
        self.choice_p = [None, self.Choice.COLOR, self.Choice.DOT]
        # player 1 is always human player
        self.choice_p[1] = choice_p1
        if self.choice_p[1] == self.Choice.COLOR:
            self.choice_p[2] = self.Choice.DOT
        else:
            self.choice_p[2] = self.Choice.COLOR

        # self.phase = self.Phase.NORMAL
        self.step = 1
        self.prev_card = None
        self.board = np.zeros((12, 8), dtype=CardSegment)

        print('Player 1 chose to play ' + self.choice_p[1].name)
        print('Player 2 will play ' + self.choice_p[2].name)
        print('==========================================')

    def place_card(self, card_type, x, y):

        is_valid_play, win_list = self.play_normal(card_type, x, y)

        if is_valid_play:
            self.step += 1
            if win_list:
                player = ((self.step - 2) % 2 + 1)
                for win in win_list:
                    if self.choice_p[player] == win[1]:
                        win = player
                win = 3 - player
                return True, self.prev_card, self.step - 1, win
                exit()
            else:
                return True, self.prev_card, self.step - 1, 0
        else:
            return False, None, self.step, 0

    def recycle_card(self, old_x1, old_y1, old_x2, old_y2, new_card_type, new_x, new_y):
        is_valid_play, win_list = self.play_recycle(old_x1, old_y1, old_x2, old_y2, new_card_type, new_x, new_y)

        if is_valid_play:
            self.step += 1
            if win_list:
                player = ((self.step - 2) % 2 + 1)
                for win in win_list:
                    if self.choice_p[player] == win[1]:
                        win = player
                win = 3 - player
                return True, self.get_card(old_x1, old_y1), self.prev_card, self.step - 1, win
                exit()
            else:
                return True, self.get_card(old_x1, old_y1), self.prev_card, self.step - 1, 0
        else:
            return False, None, None, self.step, 0

    def get_card(self, x, y):
        return self.board[y][x].parent

    def play_normal(self, card_type, x, y):
        card = Card(x, y, card_type)
        if not card.is_valid():
            return False, None
        if not self.valid_position(card):
            return False, None

        win_list = self.validate_win(card)
        self.prev_card = card
        return True, win_list

    def play_recycle(self, old_x1, old_y1, old_x2, old_y2, new_card_type, new_x, new_y):

        selected_seg1 = self.board[old_y1][old_x1]
        selected_seg2 = self.board[old_y2][old_x2]

        # check existence, check if the same card, check if the previous card
        if isinstance(selected_seg1, CardSegment) and isinstance(selected_seg2, CardSegment) and \
                selected_seg1.parent == selected_seg2.parent and selected_seg1.parent != self.prev_card:

            # if new position same as previous one, and the rotation is the same
            if selected_seg1.parent.seg[0].x == new_x and selected_seg1.parent.seg[0].y == new_y and \
                    selected_seg1.parent.card_type == new_card_type:
                return False, None

            # if remove legal
            if self.is_remove_legal(selected_seg1.parent):
                # temporarily delete the card
                self.board[old_y1][old_x1] = 0
                self.board[old_y2][old_x2] = 0
                # delegate to play_normal
                is_valid_play, win_list = self.play_normal(new_card_type, new_x, new_y)
                # restore if it's not a valid new card
                if not is_valid_play:
                    self.board[old_y1][old_x1] = selected_seg1
                    self.board[old_y2][old_x2] = selected_seg2
                return is_valid_play, win_list
        return False, None

    def is_remove_legal(self, card):
        if card.card_type % 2 == 1:
            # horizontal cards
            if card.seg[0].y < self.max_y - 1:
                # not the last row
                for seg in card.seg:
                    if isinstance(self.board[seg.y + 1][seg.x], CardSegment):
                        return False

            return True
        else:
            if card.seg[1].y < self.max_y - 1:
                if isinstance(self.board[card.seg[1].y + 1][card.seg[1].x], CardSegment):
                    return False
            return True

    def valid_position(self, card):
        # if positions empty
        for seg in card.seg:
            if isinstance(self.board[seg.y][seg.x], CardSegment):
                return False

        # temporarily set positions
        for seg in card.seg:
            self.board[seg.y][seg.x] = seg

        # check surrounding cells
        if card.seg[0].y != 0 and (not isinstance(self.board[card.seg[0].y - 1][card.seg[0].x], CardSegment)):
            for seg in card.seg:
                self.board[seg.y][seg.x] = 0
            return False

        return True

    def validate_win(self, card):
        win_list = []

        for seg in card.seg:
            for mode in self.Choice:
                # up
                count1 = self.validate_win_helper(seg, 0, 1, mode)
                # bottom
                count2 = self.validate_win_helper(seg, 0, -1, mode)
                if count1 + count2 >= 3:
                    win_list.append([seg, mode])

                # up right
                count1 = self.validate_win_helper(seg, 1, 1, mode)
                # bottom left
                count2 = self.validate_win_helper(seg, -1, -1, mode)
                if count1 + count2 >= 3:
                    win_list.append([seg, mode])

                # right
                count1 = self.validate_win_helper(seg, 1, 0, mode)
                # left
                count2 = self.validate_win_helper(seg, -1, 0, mode)
                if count1 + count2 >= 3:
                    win_list.append([seg, mode])

                # bottom right
                count1 = self.validate_win_helper(seg, 1, -1, mode)
                # top left
                count2 = self.validate_win_helper(seg, -1, 1, mode)
                if count1 + count2 >= 3:
                    win_list.append([seg, mode])

        return win_list

    def validate_win_helper(self, seg, increment_x, increment_y, mode):
        x = seg.x
        y = seg.y
        next_x = x + increment_x
        next_y = y + increment_y

        if 0 <= next_x < self.max_x and 0 <= next_y < self.max_y:
            next_seg = self.board[next_y][next_x]
            if not isinstance(next_seg, CardSegment):
                return 0
            if (mode == self.Choice.COLOR and next_seg.color == seg.color) or (
                    mode == self.Choice.DOT and next_seg.dot == seg.dot):
                count = self.validate_win_helper(next_seg, increment_x, increment_y, mode) + 1
            else:
                return 0
        else:
            return 0

        return count

    def print_board(self):
        for i in range(11, -1, -1):
            print('%3s' % str(i + 1) + ': ', end='')
            for j in range(0, 8):
                seg = self.board[i][j]
                fore = Fore.BLACK
                back = Back.RESET
                if isinstance(seg, CardSegment):
                    if seg.color == Color.RED:
                        back = Back.RED
                    else:
                        back = Back.WHITE
                    if seg.dot == Dot.SOLID:
                        symbol = '●'
                    else:
                        symbol = '○'
                    print(fore + back + symbol, end='')
                else:
                    print(' ', end='')
            print()
        print('     ABCDEFGH')


def main():
    game = Game(Game.Choice.COLOR)

    print(game.place_card(1, 0, 0))
    game.print_board()

    print(game.place_card(1,0,1))
    game.print_board()

    print(game.place_card(2,2,0))
    game.print_board()

    # invalid placement
    print(game.place_card(1,3,2))
    game.print_board()

    # invalid placement
    print(game.place_card(1,0,0))
    game.print_board()

    print(game.place_card(1,0,2))
    game.print_board()

    print(game.place_card(1,0,3))
    game.print_board()


if __name__ == '__main__':
    main()
