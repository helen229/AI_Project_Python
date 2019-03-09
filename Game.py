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
import Game_Tree
import State
from Minimax_AlphaBeta import AlphaBeta
from Mini_max import MiniMax
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

    @staticmethod
    def play_recycle(old_x1, old_y1, old_x2, old_y2, new_card_type, new_x, new_y, board, prev_card, is_game_play):

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
            if Game.is_remove_legal(selected_seg1.parent, board):
                # temporarily delete the card
                board[old_y1][old_x1] = 0
                board[old_y2][old_x2] = 0
                # delegate to play_normal
                is_valid_play, win_list, prev_card = Game.play_normal(new_card_type, new_x, new_y, board, prev_card, is_game_play)
                # restore if it's not a valid new card
                if not is_valid_play:
                    board[old_y1][old_x1] = selected_seg1
                    board[old_y2][old_x2] = selected_seg2
                return is_valid_play, win_list, prev_card
        return False, None, prev_card

    @staticmethod
    def is_remove_legal(card, board):
        if card.card_type % 2 == 1:
            # horizontal cards
            if card.seg[0].y < Game.max_y - 1:
                # not the last row
                for seg in card.seg:
                    if isinstance(board[seg.y + 1][seg.x], CardSegment):
                        return False

            return True
        else:
            if card.seg[1].y < Game.max_y - 1:
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


    def computer_move(self, choice, alg):
        time0 = time.time()
        node = State.State(None, self.board, self.step, self.prev_card)
        tree = Game_Tree.Game_Tree(node)
        tree.generateNLayerTree(node, 1)
        countH =0
        if alg=="1":
            alpha = AlphaBeta(tree,choice)
            best_Move = alpha.alpha_beta_search(tree.root)
            countH = alpha.countH
        elif alg=="2":
            mini = MiniMax(tree, choice)
            best_Move = mini.minimax(tree.root)
            countH = mini.countH
        tree.printTree(node)
        print(best_Move.val)
        print(countH)
        # print(len(best_Move.children))
        self.Print_File(countH,best_Move.val,node.children)

        if self.step < 24:
            card_removed = None
            is_valid, card_added, count, win_id = self.place_card(
                                                          best_Move.prev_card.card_type,
                                                          best_Move.prev_card.seg[0].x,
                                                          best_Move.prev_card.seg[0].y
                                                           )
        else:
            card = self.get_card(best_Move.orig_x, best_Move.orig_y)
            is_valid, card_removed, card_added, count, win_id = self.recycle_card(
                                                         best_Move.orig_x,
                                                         best_Move.orig_y,
                                                         card.seg[1].x,
                                                         card.seg[1].y,
                                                         best_Move.prev_card.card_type,
                                                         best_Move.prev_card.seg[0].x,
                                                         best_Move.prev_card.seg[0].y,
                                                         )
        time1 = time.time()
        print('copy copy: {:f}'.format(time1 - time0))
        return card_removed, card_added, count, win_id

    def Print_File(self,count, val, list):
        f = open("tracemm1.txt", "a+")
        f.write(str(count)+'\n')
        f.write(str(val)+'\r\n')
        for i in list:
            f.write(str(i.val)+'\n')
        f.write('\n')
        f.close()

#
# def main():
#     print('''
# ===============================
# Regular Move
# ===============================
#         ''')
#     game = Game(Choice.COLOR)
#
#     print(game.place_card(1, 0, 1))
#     print("Player " + str(game.get_player()))
#     Game.print_board(game.board)
#
#     print(game.place_card(1, 2, 1))
#     print("Player " + str(game.get_player()))
#     Game.print_board(game.board)
#
#     print(game.place_card(2, 2, 0))
#     print("Player " + str(game.get_player()))
#     Game.print_board(game.board)
#
#     # invalid placement
#     print(game.place_card(1, 3, 2))
#     print("Player " + str(game.get_player()))
#     Game.print_board(game.board)
#
#     # invalid placement
#     print(game.place_card(1, 0, 0))
#     print("Player " + str(game.get_player()))
#     Game.print_board(game.board)
#
#     print(game.place_card(1, 0, 2))
#     print("Player " + str(game.get_player()))
#     Game.print_board(game.board)
#
#     print(game.place_card(7, 0, 3))
#     print("Player " + str(game.get_player()))
#     Game.print_board(game.board)
#
#     print('''
# ===============================
# Test Recycling
# ===============================
#     ''')
#     game = Game(Choice.COLOR)
#     card_type = [1, 5, 3, 7, 1, 5]
#     for i in range(6):
#         for j in range(0, 7, 2):
#             print(game.place_card(card_type[i], j, i))
#
#     Game.print_board(game.board)
#
#     # invalid
#     print(game.recycle_card(6, 5, 7, 5, 2, 0, 6))
#     Game.print_board(game.board)
#
#     print(game.recycle_card(4, 5, 5, 5, 2, 0, 6))
#     Game.print_board(game.board)
#
#     print('''
#     ===============================
#     Test Recycling
#     ===============================
#         ''')
    # new_board = np.copy(game.board)
    # game.board[5][7].color = Color.RED
    #
    # print("Original Board")
    # game.print_board()
    #
    # print("Copied Board")
    # print(new_board[5][7])

    # # test deep copy speed
    # time0 = time.time()
    # for i in range(10000):
    #     tmp = np.copy(game.board)
    #     card=Card(0,1,8)
    # time1 = time.time()
    #
    # print('np copy: {:f}'.format(time1 - time0))
    #
    # time0 = time.time()
    # for i in range(10000):
    #     tmp = copy.copy(game.board)
    #     card = Card(0, 1, 8)
    # time1 = time.time()
    #
    # print('copy copy: {:f}'.format(time1 - time0))

    # time0 = time.time()
    # for i in range(10000):
    #     tmp = copy.deepcopy(game.board)
    # time1 = time.time()
    #
    # print('deep copy: {:f}'.format(time1 - time0))


# if __name__ == '__main__':
#     main()