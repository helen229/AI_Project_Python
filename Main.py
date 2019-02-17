"""
main function
"""
# print ('Number of arguments:"', len(sys.argv), 'arguments.')
# print ('Argument List:"', str(sys.argv))
import sys
import re
import numpy as np
from sys import argv
from enum import Enum
from Card import Card
from CardSegment import CardSegment
from CardSegment import Color
from CardSegment import Dot
from colorama import init
from colorama import Fore, Back, Style

max_x = 8
max_y = 12

init(autoreset=True)


class Phase(Enum):
    NORMAL = 1
    RECYCLE = 2


class Choice(Enum):
    COLOR = 1
    DOT = 2


def main():
    choice_p = [None, Choice.COLOR, Choice.DOT]

    while True:
        user_input = input('Player 1: play color or dot? (1-Color, 2-Dot): ')
        choice = re.match('^([1-2])$', user_input)
        if choice:
            choice_p[1] = Choice(int(choice.group(1)))
            if choice_p[1] == Choice.COLOR:
                choice_p[2] = Choice.DOT
            else:
                choice_p[2] = Choice.COLOR
            print('Player 1 chose to play ' + choice_p[1].name)
            print('Player 2 will play ' + choice_p[2].name)
            print('==========================================')
            break

        print('Invalid input, please try again')

    phase = Phase.NORMAL
    step = 1
    seg_board = np.zeros((12, 8), dtype=CardSegment)
    pattern = [re.compile('^(0)\\s([1-8])\\s([A-H])\\s([1-9]|1[0-2])$'),
               re.compile('^([A-H])\\s([1-9]|1[0-2])\\s([A-H])\\s([1-9]|1[0-2])\\s([1-8])\\s([A-H])\\s([1-9]|1[0-2])$')]

    while True:

        param = None
        is_valid_play = False
        is_win = False
        player = 1
        while (not param) or (not is_valid_play):
            player = ((step - 1) % 2 + 1)
            user_input = input('Player ' + str(player) + ' [' + phase.name + ']: ')
            param = pattern[phase.value - 1].match(user_input)
            if not param:
                print('Invalid input, please try again')
                continue
            if param.group(1) == '0':
                is_valid_play, prev_card, win_list = play_normal(param[2], param[3], param[4], seg_board, player)
            else:
                is_valid_play, prev_card, win_list = play_recycle(param, seg_board, player, prev_card)

            if not is_valid_play:
                print('Invalid positions, please try again')

        print_board(seg_board)

        if win_list:
            for win in win_list:
                if choice_p[player] == win[1]:
                    print('Player ' + str(player) + ' wins!')
                    exit()
            print('Player ' + str(3 - player) + ' wins!')
            exit()

        if step == 60:
            print('Game ends in a draw')
            exit()
        if step == 24:
            print('Recycling phase starts')
            phase = Phase.RECYCLE
        step += 1


def play_normal(card_type, px, py, seg_board, player):
    card = Card(px, py, card_type, player)
    if not card.is_valid():
        return False, None, None
    if not valid_position(card, seg_board):
        return False, None, None

    win_list = validate_win(card, seg_board)

    return True, card, win_list


def play_recycle(param, seg_board, player, prev_card):
    px1 = ord(param[1]) - 65
    py1 = int(param[2]) - 1
    px2 = ord(param[3]) - 65
    py2 = int(param[4]) - 1

    new_card_type = param[5]
    new_px = param[6]
    new_py = param[7]

    selected_seg1 = seg_board[py1][px1]
    selected_seg2 = seg_board[py2][px2]

    # if new position same as previous one, and the rotation is the same
    if param[1] == param[6] and param[2] == param[7] and selected_seg1.parent.card_type == int(new_card_type):
        return False, None, None

    # check existence, check if the same card, check if the previous card
    if isinstance(selected_seg1, CardSegment) and isinstance(selected_seg2, CardSegment) and \
            selected_seg1.parent == selected_seg2.parent and selected_seg1.parent != prev_card:
        # if remove legal
        if is_remove_legal(selected_seg1, seg_board) and is_remove_legal(selected_seg2, seg_board):
            # temporarily delete the card
            seg_board[py1][px1] = 0
            seg_board[py2][px2] = 0
            # delegate to play_normal
            is_valid_play, prev_card, win_list = play_normal(new_card_type, new_px, new_py, seg_board, player)
            # restore if it's not a valid new card
            if not is_valid_play:
                seg_board[py1][px1] = selected_seg1
                seg_board[py2][px2] = selected_seg2
            return is_valid_play, prev_card, win_list
    return False, None, None


def is_remove_legal(segment, seg_board):
    seg_above = seg_board[segment.y + 1][segment.x]
    if isinstance(seg_above, CardSegment):
        return False
    else:
        return True


def valid_position(card, seg_board):
    # if positions empty
    for seg in card.seg:
        if isinstance(seg_board[seg.y][seg.x], CardSegment):
            return False

    # temporarily set positions
    for seg in card.seg:
        seg_board[seg.y][seg.x] = seg

    # check surrounding cells
    if seg.y != 0 and (not isinstance(seg_board[seg.y - 1][seg.x], CardSegment)):
        for seg in card.seg:
            seg_board[seg.y][seg.x] = 0
        return False

    return True


def validate_win(card, seg_board):
    win_list = []

    for seg in card.seg:
        for mode in Choice:
            # up
            count1 = validate_win_helper(seg, 0, 1, seg_board, mode)
            # bottom
            count2 = validate_win_helper(seg, 0, -1, seg_board, mode)
            if count1 + count2 >= 3:
                win_list.append([seg, mode])

            # up right
            count1 = validate_win_helper(seg, 1, 1, seg_board, mode)
            # bottom left
            count2 = validate_win_helper(seg, -1, -1, seg_board, mode)
            if count1 + count2 >= 3:
                win_list.append([seg, mode])

            # right
            count1 = validate_win_helper(seg, 1, 0, seg_board, mode)
            # left
            count2 = validate_win_helper(seg, -1, 0, seg_board, mode)
            if count1 + count2 >= 3:
                win_list.append([seg, mode])

            # bottom right
            count1 = validate_win_helper(seg, 1, -1, seg_board, mode)
            # top left
            count2 = validate_win_helper(seg, -1, 1, seg_board, mode)
            if count1 + count2 >= 3:
                win_list.append([seg, mode])

    return win_list


def validate_win_helper(seg, increment_x, increment_y, seg_board, mode):
    x = seg.x
    y = seg.y
    next_x = x + increment_x
    next_y = y + increment_y

    if 0 <= next_x < max_x and 0 <= next_y < max_y:
        next_seg = seg_board[next_y][next_x]
        if not isinstance(next_seg, CardSegment):
            return 0
        if (mode == Choice.COLOR and next_seg.color == seg.color) or (
                mode == Choice.DOT and next_seg.dot == seg.dot):
            count = validate_win_helper(next_seg, increment_x, increment_y, seg_board, mode) + 1
        else:
            return 0
    else:
        return 0

    return count


def print_board(seg_board):
    for i in range(11, -1, -1):
        print('%3s' % str(i+1) + ': ', end='')
        for j in range(0, 8):
            seg = seg_board[i][j]
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
                print(fore+back+symbol, end='')
            else:
                print(' ', end='')
        print()
    print('     ABCDEFGH')


if __name__ == '__main__':
    main()
