"""
main function
"""
# print ('Number of arguments:"', len(sys.argv), 'arguments.')
# print ('Argument List:"', str(sys.argv))
import sys
import numpy as np
from sys import argv
import Card

def main():
    count = 0
    map = np.zeros((12, 8))
    IdMap=np.zeros((12, 8))
    test_Dict = {}
    while 1:
        if count==24:
            print('Start recleying')
            break;
        if count==60:
            print('this is draw')
            break;

        if count % 2==0:
            print('Player1 Please enter your type and positon:')
        else:
            print('Player2 Please enter your type and positon:')

        para = input()
        para = para.replace(" ","")

        idk = para[0]
        type = int(para[1])
        px = ord(para[2])-65
        py = int(para[3])-1

        type1, type2, px2, py2 = TypeConvert(py,px,type)

        #if validate then count++
        count += 1

        # print(type)
        # print(px)
        # print(py)

        p1 = Card.Card(type1, px, py, count)
        p2 = Card.Card(type2, px2, py2, count)


        test_Dict[p1] = count
        test_Dict[p2] = count
        CardList=test_Dict.keys()
        print(list(CardList)[1].x)
        print(list(CardList)[1].y)
        print(list(CardList)[1].attribute)

        map[py][px] = type1
        map[py2][px2] = type2

        IdMap[py][px] = count
        IdMap[py2][px2] = count
        print(IdMap)
        print()

        if (bfs(py2, px2, py2 + 1, px2, type, 1, 2, map, 0) or
        bfs(py2, px2, py2 - 1, px2, type, 1, 2, map, 0) or
        bfs(py2, px2, py2, px2 + 1, type, 3, 4, map, 0) or
        bfs(py2, px2, py2, px2 - 1, type, 3, 4, map, 0) or
        bfs(py2, px2, py2 + 1, px2 + 1, type, 5, 7, map, 0) or
        bfs(py2, px2, py2 - 1, px2 + 1, type, 6, 8, map, 0) or
        bfs(py2, px2, py2 - 1, px2 - 1, type, 5, 7, map, 0) or
        bfs(py2, px2, py2 + 1, px2 - 1, type, 6, 8, map, 0) or
        bfs(py, px, py + 1, px, type, 1, 2, map, 0) or
        bfs(py, px, py - 1, px, type, 1, 2, map, 0) or
        bfs(py, px, py, px + 1, type, 3, 4, map, 0) or
        bfs(py, px, py, px - 1, type, 3, 4, map, 0) or
        bfs(py, px, py + 1, px + 1, type, 5, 7, map, 0) or
        bfs(py, px, py - 1, px + 1, type, 6, 8, map, 0) or
        bfs(py, px, py - 1, px - 1, type, 5, 7, map, 0) or
        bfs(py, px, py + 1, px - 1, type, 6, 8, map, 0)):
            break

        print(map)

# according the type to calculate the two half type and position
def TypeConvert(py,px,type):
    type1=-1
    type2=-1
    px2 = -1
    py2 = -1
    if type==1:
        type1=2
        type2=3
        px2 = px+1
        py2 = py
    elif type==2:
        type1=3
        type2=2
        px2 = px
        py2 = py+1
    elif type==3:
        type1=3
        type2=2
        px2 = px+1
        py2 = py
    elif type == 4:
        type1 = 2
        type2 = 3
        px2 = px
        py2 = py+1
    elif type==5:
        type1=1
        type2=4
        px2 = px+1
        py2 = py
    elif type==6:
        type1=4
        type2=1
        px2 = px
        py2 = py+1
    elif type==7:
        type1=4
        type2=1
        px2 = px+1
        py2 = py
    elif type==8:
        type1=1
        type2=4
        px2 = px+1
        py2 = py
    else:
        print("Wrong Type")

    return type1, type2, px2, py2;


# first choose (py,px) as start point and choose a adjacent node to compare,
# if same value then do the dfs for two direction
def bfs(py,px,py2,px2,type,direction1,direction2, map, count):
    if py2 < 0 or py2 > 11 or px2 < 0 or px2 > 7 or map[py][px] != map[py2][px2]:
        return False
    # count the same value : vertically, horizontally, or diagonally
    count = dfs(py, px, map[py][px], direction1, map, 0) + dfs(py, px, map[py][px], direction2, map, 0) - 1
    if count == 4:
        print(map[py][px]," win")
        return True
    else:
        # print(map[py2][px2])
        print("Not Win Count=", count)

# start dfs from py,px and return the number of adjacent same vale
def dfs(py, px, type, direction, map, result):
    if py<0 or py>11 or px<0 or px>7:
        return result
    if map[py][px] == type:
        result += 1
    else:
        return result

    if direction == 1:
        py += 1;
    elif direction == 2:
        py -= 1;
    elif direction == 3:
        px += 1;
    elif direction == 4:
        px -= 1;
    elif direction == 5:
        px += 1;
        py += 1;
    elif direction == 6:
        px += 1;
        py -= 1;
    elif direction == 7:
        px -= 1;
        py -= 1;
    elif direction == 8:
        px -= 1;
        py += 1;

    result=dfs(py, px, type, direction, map, result)
    return result


if __name__ == '__main__':
    main()
