"""
Game class
"""

import numpy as np
import copy
import time
from enum import Enum
from Card import Card
from CardSegment import CardSegment
from CardSegment import Color
from CardSegment import Dot
from colorama import init
from colorama import Fore, Back, Style
from Game_Tree import Game_Tree
from State import State
from Minimax_AlphaBeta import AlphaBeta

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
        self.choice_p = [None, Choice.COLOR, Choice.DOT]
        # player 1 is always human player
        self.choice_p[1] = choice_p1
        if self.choice_p[1] == Choice.COLOR:
            self.choice_p[2] = Choice.DOT
        else:
            self.choice_p[2] = Choice.COLOR

        # self.phase = self.Phase.NORMAL
        self.step = 1
        self.prev_card = None
        self.board = np.zeros((12, 8), dtype=CardSegment)

        print('Player 1 chose to play ' + self.choice_p[1].name)
        print('Player 2 will play ' + self.choice_p[2].name)
        print('==========================================')

    def place_card(self, card_type, x, y):

        is_valid_play, win_list, self.prev_card = self.play_normal(card_type, x, y, self.board, self.prev_card, True)

        if is_valid_play:
            self.step += 1
            if win_list:
                player = self.get_player()
                win_player = -1
                for win in win_list:
                    if self.choice_p[player] == win[1]:
                        win_player = player
                if win_player == -1:
                    win_player = 3 - player
                return True, self.prev_card, self.step - 1, win_player
            else:
                return True, self.prev_card, self.step - 1, 0
        else:
            return False, None, self.step, 0

    def recycle_card(self, old_x1, old_y1, old_x2, old_y2, new_card_type, new_x, new_y):
        old_seg = self.board[old_y1][old_x1]

        is_valid_play, win_list, self.prev_card = self.play_recycle(old_x1, old_y1, old_x2, old_y2, new_card_type, new_x, new_y, self.board, self.prev_card, True)

        if is_valid_play:
            self.step += 1
            if win_list:
                player = self.get_player()
                win_player = -1
                for win in win_list:
                    if self.choice_p[player] == win[1]:
                        win_player = player
                if win_player == -1:
                    win_player = 3 - player
                return True, old_seg.parent, self.prev_card, self.step - 1, win_player
            else:
                return True, old_seg.parent, self.prev_card, self.step - 1, 0
        else:
            return False, None, None, self.step, 0

    def get_player(self):
        return (self.step - 2) % 2 + 1

    def get_card(self, x, y):
        return self.board[y][x].parent

    @staticmethod
    def play_normal(card_type, x, y, board, prev_card, is_game_play):
        card = Card(x, y, card_type)
        if not card.is_valid():
            return False, None, prev_card
        if not Game.valid_position(card, board):
            return False, None, prev_card

        if is_game_play:
            win_list = Game.validate_win(card, board)
            return True, win_list, card
        else:
            return True, None, card

    def play_recycle(self, old_x1, old_y1, old_x2, old_y2, new_card_type, new_x, new_y, board, prev_card, is_game_play):

        selected_seg1 = board[old_y1][old_x1]
        selected_seg2 = board[old_y2][old_x2]

        # check existence, check if the same card, check if the previous card
        if isinstance(selected_seg1, CardSegment) and isinstance(selected_seg2, CardSegment) and \
                selected_seg1.parent == selected_seg2.parent and selected_seg1.parent != prev_card:

            # if new position same as previous one, and the rotation is the same
            if selected_seg1.parent.seg[0].x == new_x and selected_seg1.parent.seg[0].y == new_y and \
                    selected_seg1.parent.card_type == new_card_type:
                return False, None, prev_card

            # if remove legal
            if self.is_remove_legal(selected_seg1.parent, board):
                # temporarily delete the card
                board[old_y1][old_x1] = 0
                board[old_y2][old_x2] = 0
                # delegate to play_normal
                is_valid_play, win_list, prev_card = self.play_normal(new_card_type, new_x, new_y, board, prev_card, is_game_play)
                # restore if it's not a valid new card
                if not is_valid_play:
                    board[old_y1][old_x1] = selected_seg1
                    board[old_y2][old_x2] = selected_seg2
                return is_valid_play, win_list, prev_card
        return False, None, prev_card

    def is_remove_legal(self, card, board):
        if card.card_type % 2 == 1:
            # horizontal cards
            if card.seg[0].y < self.max_y - 1:
                # not the last row
                for seg in card.seg:
                    if isinstance(board[seg.y + 1][seg.x], CardSegment):
                        return False

            return True
        else:
            if card.seg[1].y < self.max_y - 1:
                if isinstance(board[card.seg[1].y + 1][card.seg[1].x], CardSegment):
                    return False
            return True

    @staticmethod
    def valid_position(card, board):
        # if positions empty
        for seg in card.seg:
            if isinstance(board[seg.y][seg.x], CardSegment):
                return False

        # temporarily set positions
        for seg in card.seg:
            board[seg.y][seg.x] = seg

        # check surrounding cells
        if card.seg[0].y != 0:
            if (not isinstance(board[card.seg[0].y - 1][card.seg[0].x], CardSegment)) or \
                    (not isinstance(board[card.seg[1].y - 1][card.seg[1].x], CardSegment)):
                for seg in card.seg:
                    board[seg.y][seg.x] = 0
                return False

        return True

    @staticmethod
    def validate_win(card, board):
        win_list = []

        for seg in card.seg:
            for mode in Choice:
                # up
                count1 = Game.validate_win_helper(seg, 0, 1, mode, board)
                # bottom
                count2 = Game.validate_win_helper(seg, 0, -1, mode, board)
                if count1 + count2 >= 3:
                    win_list.append([seg, mode])

                # up right
                count1 = Game.validate_win_helper(seg, 1, 1, mode, board)
                # bottom left
                count2 = Game.validate_win_helper(seg, -1, -1, mode, board)
                if count1 + count2 >= 3:
                    win_list.append([seg, mode])

                # right
                count1 = Game.validate_win_helper(seg, 1, 0, mode, board)
                # left
                count2 = Game.validate_win_helper(seg, -1, 0, mode, board)
                if count1 + count2 >= 3:
                    win_list.append([seg, mode])

                # bottom right
                count1 = Game.validate_win_helper(seg, 1, -1, mode, board)
                # top left
                count2 = Game.validate_win_helper(seg, -1, 1, mode, board)
                if count1 + count2 >= 3:
                    win_list.append([seg, mode])

        return win_list

    @staticmethod
    def validate_win_helper(seg, increment_x, increment_y, mode, board):
        x = seg.x
        y = seg.y
        next_x = x + increment_x
        next_y = y + increment_y

        if 0 <= next_x < Game.max_x and 0 <= next_y < Game.max_y:
            next_seg = board[next_y][next_x]
            if not isinstance(next_seg, CardSegment):
                return 0
            if (mode == Choice.COLOR and next_seg.color == seg.color) or (
                    mode == Choice.DOT and next_seg.dot == seg.dot):
                count = Game.validate_win_helper(next_seg, increment_x, increment_y, mode, board) + 1
            else:
                return 0
        else:
            return 0

        return count

    @staticmethod
    def print_board(board):
        for i in range(11, -1, -1):
            print('%3s' % str(i + 1) + ': ', end='')
            for j in range(0, 8):
                seg = board[i][j]
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

    def computer_move(self):
        node = State(None, self.board, self.step, self.prev_card)
        tree = Game_Tree(node)
        print("tree start")
        tree.generateNLayerTree(node, 2)
        print("tree finsh")
        # best_Move = AlphaBeta(tree).alpha_beta_search(tree.root)
        # card = best_Move.prev_card
        # count = best_Move.step
        win_id = 0
        return None, 2, win_id
