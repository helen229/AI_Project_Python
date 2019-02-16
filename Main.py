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

max_x = 8
max_y = 12


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
    card_board = np.zeros((12, 8), dtype=Card)
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
                is_valid_play, win_list = play_normal(param, card_board, seg_board, player)
            # else:
            #    is_valid_play, win_list = play_recycle(param, card_board, seg_board, player)

            if not is_valid_play:
                print('Invalid positions, please try again')

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


def play_normal(param, card_board, seg_board, player):
    card_type = int(param[2])
    px = param[3]
    py = int(param[4])

    card = Card(px, py, card_type, player)
    if not card.is_valid():
        return False, None
    if not valid_position(card, seg_board):
        return False, None

    # seg_board has already been assigned to segments in valid_position()
    for seg in card.seg:
        card_board[seg.y][seg.x] = card

    win_list = validate_win(card, card_board, seg_board)

    return True, win_list


def play_recycle(param, card_board, seg_board, player):

      return True, None


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


def validate_win(card, card_board, seg_board):
    win_list = []

    for seg in card.seg:
        for mode in Choice:
            # up
            count1 = validate_win_helper(seg, 0, 1, card_board, seg_board, mode)
            # bottom
            count2 = validate_win_helper(seg, 0, -1, card_board, seg_board, mode)
            if count1 + count2 >= 3:
                win_list.append([seg, mode])

            # up right
            count1 = validate_win_helper(seg, 1, 1, card_board, seg_board, mode)
            # bottom left
            count2 = validate_win_helper(seg, -1, -1, card_board, seg_board, mode)
            if count1 + count2 >= 3:
                win_list.append([seg, mode])

            # right
            count1 = validate_win_helper(seg, 1, 0, card_board, seg_board, mode)
            # left
            count2 = validate_win_helper(seg, -1, 0, card_board, seg_board, mode)
            if count1 + count2 >= 3:
                win_list.append([seg, mode])

            # bottom right
            count1 = validate_win_helper(seg, 1, -1, card_board, seg_board, mode)
            # top left
            count2 = validate_win_helper(seg, -1, 1, card_board, seg_board, mode)
            if count1 + count2 >= 3:
                win_list.append([seg, mode])

    return win_list


def validate_win_helper(seg, increment_x, increment_y, card_board, seg_board, mode):
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
            count = validate_win_helper(next_seg, increment_x, increment_y, card_board, seg_board, mode) + 1
        else:
            return 0
    else:
        return 0

    return count


if __name__ == '__main__':
    main()
