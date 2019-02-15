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
import Card


class Phase(Enum):
    NORMAL = 1
    RECYCLE = 2


def main():
    phase = Phase.NORMAL
    count = 0
    board = np.zeros((12, 8))
    id_board = np.zeros((12, 8))
    test_dict = {}
    pattern = [re.compile('^0\\s([1-8])\\s([A-H])\\s([1-9]|1[0-2])$'),
               re.compile('^([A-H])\\s([1-9]|1[0-2])\\s([A-H])\\s([1-9]|1[0-2])\\s([1-8])\\s([A-H])\\s([1-9]|1[0-2])$')]

    while 1:
        if phase == Phase.NORMAL and count == 24:
            print('Recycling phase starts')
            phase = Phase.RECYCLE
            break
        elif count == 60:
            print('Game ends in a draw')
            break

        param = None
        while not param:
            print('Player' + str(((count % 2) + 1)) + ' [' + phase.name + ']: ')
            user_input = input()
            param = pattern[phase.value-1].match(user_input)
            if not param:
                print("Invalid input, please try again")

        idk = param[0]
        type = int(param[1])
        px = ord(param[2]) - 65
        py = int(param[3]) - 1

        type1, type2, px2, py2 = TypeConvert(py, px, type)

        # if validate then count++
        count += 1

        # print(type)
        # print(px)
        # print(py)

        p1 = Card.Card(type1, px, py, count)
        p2 = Card.Card(type2, px2, py2, count)

        test_dict[p1] = count
        test_dict[p2] = count
        CardList = test_dict.keys()
        print(list(CardList)[1].x)
        print(list(CardList)[1].y)
        print(list(CardList)[1].attribute)

        board[py][px] = type1
        board[py2][px2] = type2

        id_board[py][px] = count
        id_board[py2][px2] = count
        print(id_board)
        print()

        if (bfs(py2, px2, py2 + 1, px2, type, 1, 2, board, 0) or
                bfs(py2, px2, py2 - 1, px2, type, 1, 2, board, 0) or
                bfs(py2, px2, py2, px2 + 1, type, 3, 4, board, 0) or
                bfs(py2, px2, py2, px2 - 1, type, 3, 4, board, 0) or
                bfs(py2, px2, py2 + 1, px2 + 1, type, 5, 7, board, 0) or
                bfs(py2, px2, py2 - 1, px2 + 1, type, 6, 8, board, 0) or
                bfs(py2, px2, py2 - 1, px2 - 1, type, 5, 7, board, 0) or
                bfs(py2, px2, py2 + 1, px2 - 1, type, 6, 8, board, 0) or
                bfs(py, px, py + 1, px, type, 1, 2, board, 0) or
                bfs(py, px, py - 1, px, type, 1, 2, board, 0) or
                bfs(py, px, py, px + 1, type, 3, 4, board, 0) or
                bfs(py, px, py, px - 1, type, 3, 4, board, 0) or
                bfs(py, px, py + 1, px + 1, type, 5, 7, board, 0) or
                bfs(py, px, py - 1, px + 1, type, 6, 8, board, 0) or
                bfs(py, px, py - 1, px - 1, type, 5, 7, board, 0) or
                bfs(py, px, py + 1, px - 1, type, 6, 8, board, 0)):
            break

        print(board)


# according the type to calculate the two half type and position
def TypeConvert(py, px, type):
    type1 = -1
    type2 = -1
    px2 = -1
    py2 = -1
    if type == 1:
        type1 = 2
        type2 = 3
        px2 = px + 1
        py2 = py
    elif type == 2:
        type1 = 3
        type2 = 2
        px2 = px
        py2 = py + 1
    elif type == 3:
        type1 = 3
        type2 = 2
        px2 = px + 1
        py2 = py
    elif type == 4:
        type1 = 2
        type2 = 3
        px2 = px
        py2 = py + 1
    elif type == 5:
        type1 = 1
        type2 = 4
        px2 = px + 1
        py2 = py
    elif type == 6:
        type1 = 4
        type2 = 1
        px2 = px
        py2 = py + 1
    elif type == 7:
        type1 = 4
        type2 = 1
        px2 = px + 1
        py2 = py
    elif type == 8:
        type1 = 1
        type2 = 4
        px2 = px + 1
        py2 = py
    else:
        print("Wrong Type")

    return type1, type2, px2, py2


# first choose (py,px) as start point and choose a adjacent node to compare,
# if same value then do the dfs for two direction
def bfs(py, px, py2, px2, type, direction1, direction2, map, count):
    if py2 < 0 or py2 > 11 or px2 < 0 or px2 > 7 or map[py][px] != map[py2][px2]:
        return False
    # count the same value : vertically, horizontally, or diagonally
    count = dfs(py, px, map[py][px], direction1, map, 0) + dfs(py, px, map[py][px], direction2, map, 0) - 1
    if count == 4:
        print(map[py][px], " win")
        return True
    else:
        # print(map[py2][px2])
        print("Not Win Count=", count)


# start dfs from py,px and return the number of adjacent same vale
def dfs(py, px, type, direction, map, result):
    if py < 0 or py > 11 or px < 0 or px > 7:
        return result
    if map[py][px] == type:
        result += 1
    else:
        return result

    if direction == 1:
        py += 1
    elif direction == 2:
        py -= 1
    elif direction == 3:
        px += 1
    elif direction == 4:
        px -= 1
    elif direction == 5:
        px += 1
        py += 1
    elif direction == 6:
        px += 1
        py -= 1
    elif direction == 7:
        px -= 1
        py -= 1
    elif direction == 8:
        px -= 1
        py += 1

    result = dfs(py, px, type, direction, map, result)
    return result


if __name__ == '__main__':
    main()
