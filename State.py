import numpy as np

from CardSegment import CardSegment
from CardSegment import Color
from CardSegment import Dot
import Game

connection_value = [10, 100, 1000, 10000, 10000]
cost_every_gap = 1


class State:

    def __init__(self, parent, board, step, prev_card, orig_x=None, orig_y=None):
        """
        Ctor for State class
        :param parent: parent State, can be None for the root node
        :param board: based on which board create the board of current state
        :param step: the count of steps of the this State
        :param prev_card: the most recent card has been placed in the previous step
        :param orig_x: x index of original card in recycling phase
        :param orig_y: y index of original card in recycling phase
        """
        self.board = np.copy(board)
        self.step = step
        self.prev_card = prev_card
        self.orig_x = orig_x
        self.orig_y = orig_y
        self.parent = parent
        self.children = []
        self.highest_row = [-1] * 8
        self.is_win = False
        self.val=0

    def generate_children(self):
        """
        Generate children state for a state node and add it the current node's children list
        """
        if self.step < 24:
            self.generate_regular_move(True)
        else:
            self.generate_recycle_move()

    def generate_regular_move(self, check_win):

        if self.is_win:
            return

        if self.highest_row[0] == -1:
            self.find_highest_row()

        for i in range(8):
            # still have empty cell on this column
            if self.highest_row[i] < 12:
                for t in range(1, 9):
                    new_board = np.copy(self.board)
                    is_valid_play, win_list, prev_card = Game.Game.play_normal(t, i, self.highest_row[i], new_board,
                                                                               self.prev_card, check_win)
                    if is_valid_play:
                        state = State(self, new_board, self.step + 1, prev_card)
                        self.children.append(state)
                        if win_list:
                            self.is_win = True

    def generate_recycle_move(self):

        if self.is_win:
            return

        self.generate_regular_move(False)

        # put states into matrix of column index(y) and type id(x)
        cache = np.zeros((8, 8), dtype=State)
        for child in self.children:
            card = child.prev_card
            cache[card.seg[0].x][card.card_type - 1] = child
        self.children.clear()

        card = None

        # create recycle moves
        for i in range(8):

            # skip if it's a horizontal card and just processed with its another half
            if card and card.card_type % 2 == 1 and i - 1 == card.seg[0].x:
                continue

            # skip empty column
            if self.highest_row[i] == 0:
                continue

            card = self.board[self.highest_row[i] - 1][i].parent

            # skip if it's the prev_card
            if card == self.prev_card:
                continue

            # skip if the card is makes other cards hanging
            if not Game.Game.is_remove_legal(card, self.board):
                continue

            old_x1 = card.seg[0].x
            old_y1 = card.seg[0].y
            old_x2 = card.seg[1].x
            old_y2 = card.seg[1].y

            # j - column of new placement
            for j in range(8):
                for t in range(1, 9):
                    if j == old_x1 or j == old_x2 or (j == old_x1 - 1 and t % 2 == 1):
                        new_board = np.copy(self.board)
                        is_valid_play, win_list, prev_card = Game.Game.play_recycle(old_x1, old_y1, old_x2, old_y2, t,
                                                                                    j, old_y1, new_board,
                                                                                    self.prev_card, True)
                        if is_valid_play:
                            state = State(self, new_board, self.step + 1, prev_card, j, old_y1)
                            self.children.append(state)

                    else:
                        s = cache[j][t - 1]
                        if isinstance(s, State):
                            new_board = np.copy(s.board)
                            for seg in card.seg:
                                new_board[seg.y][seg.x] = 0
                            state = State(self, new_board, s.step, s.prev_card, old_x1, old_y1)
                            self.children.append(state)

                            if Game.Game.validate_win(s.prev_card, s.board):
                                self.is_win = True

    def find_highest_row(self):
        for j in range(8):
            for i in range(12):
                if not isinstance(self.board[i][j], CardSegment):
                    self.highest_row[j] = i
                    break
            if self.highest_row[j] == -1:
                self.highest_row[j] = 12

    def get_Heuristic(self):
        sum = 0
        for j in range(8):
            for i in range(12):
                if isinstance(self.board[i][j], CardSegment):
                    coordinates_Val = i * 10 + j + 1
                    if (self.board[i][j].color == Color.WHITE and self.board[i][j].dot == Dot.EMPTY):
                        sum += coordinates_Val
                    if (self.board[i][j].color == Color.WHITE and self.board[i][j].dot == Dot.SOLID):
                        sum += 3 * coordinates_Val
                    if (self.board[i][j].color == Color.RED and self.board[i][j].dot == Dot.SOLID):
                        sum -= 2 * coordinates_Val
                    if (self.board[i][j].color == Color.RED and self.board[i][j].dot == Dot.EMPTY):
                        sum -= 1.5 * coordinates_Val
        return sum

    def get_H(self, AI_choice):

        if self.highest_row[0] == -1:
            self.find_highest_row()

        H = 0

        for j in range(8):

            curr_col = self.highest_row[j]-1
            if curr_col < 0:
                continue

            prev_col = -2
            next_col = -2

            if j-1>=0:
                prev_col = self.highest_row[j-1]-1
            if j+1<=7:
                next_col = self.highest_row[j+1]-1

            seg = self.board[curr_col][j]

            # -> \ AND left edge
            if prev_col != -2:
                # ->
                if prev_col < curr_col:
                    for mode in Game.Choice:
                        count = State.count_helper(seg, 1, 0, mode, self.board)
                        extra_cost = 0

                        if count > 0 and curr_col-prev_col > 2:
                            extra_cost = ((curr_col-prev_col+1)//2)*cost_every_gap

                        value = connection_value[count] - extra_cost

                        if count >= 3 and mode == AI_choice:
                            value = 99999

                        if mode.value == 1:
                            H += value
                        else:
                            H -= value

                    # left edge
                    for i in range(prev_col+1,curr_col):
                        seg_edge = self.board[i][j]
                        count = State.count_helper(seg_edge, 1, 0, mode, self.board)
                        extra_cost = 0

                        if count > 0 and i-prev_col > 2:
                            extra_cost = ((i-prev_col+1)//2)*cost_every_gap

                        value = connection_value[count] - extra_cost

                        if count >= 3 and mode == AI_choice:
                            value = 99999

                        if mode.value == 1:
                            H += value
                        else:
                            H -= value

                # \
                if prev_col <= curr_col:
                    for mode in Game.Choice:
                        count = State.count_helper(seg, 1, -1, mode, self.board)
                        extra_cost = 0

                        if count > 0 and curr_col - prev_col > 1:
                            extra_cost = ((curr_col - prev_col + 1) // 2) * cost_every_gap

                        value = connection_value[count] - extra_cost

                        if count >= 3 and mode == AI_choice:
                            value = 99999

                        if mode.value == 1:
                            H += value
                        else:
                            H -= value

            # |
            for mode in Game.Choice:
                count = State.count_helper(seg, 0, -1, mode, self.board)
                value = connection_value[count]

                if count >= 3 and mode == AI_choice:
                    value = 99999

                if mode.value == 1:
                    H += value
                else:
                    H -= value

            # / <-
            if next_col != -2:
                # <-
                if next_col < curr_col:
                    for mode in Game.Choice:
                        count = State.count_helper(seg, -1, 0, mode, self.board)
                        extra_cost = 0

                        if count > 0 and curr_col - next_col > 2:
                            extra_cost = ((curr_col - next_col + 1) // 2) * cost_every_gap

                        value = connection_value[count] - extra_cost

                        if count >= 3 and mode == AI_choice:
                            value = 99999

                        if mode.value == 1:
                            H += value
                        else:
                            H -= value

                    # right edge
                    for i in range(next_col+1, curr_col):
                        seg_edge = self.board[i][j]
                        count = State.count_helper(seg_edge, -1, 0, mode, self.board)
                        extra_cost = 0

                        if count > 0 and i-next_col > 2:
                            extra_cost = ((i-next_col+1)//2)*cost_every_gap

                        value = connection_value[count] - extra_cost

                        if count >= 3 and mode == AI_choice:
                            value = 99999

                        if mode.value == 1:
                            H += value
                        else:
                            H -= value

                # /
                if next_col <= curr_col:
                    for mode in Game.Choice:
                        count = State.count_helper(seg, -1, -1, mode, self.board)
                        extra_cost = 0

                        if count > 0 and curr_col - next_col > 1:
                            extra_cost = ((curr_col - prev_col + 1) // 2) * cost_every_gap

                        value = connection_value[count] - extra_cost
                        if count >= 3 and mode == AI_choice:
                            value = 99999

                        if mode.value == 1:
                            H += value
                        else:
                            H -= value
        # print(str(H))
        return H


    @staticmethod
    def count_connection(x, y, board):
        # 1st row: color; 2nd row: dot
        result = np.zeros((2, 4), dtype=int)

        seg = board[y][x]

        for mode in Game.Choice:
            # up
            count1 = State.count_helper(seg, 0, 1, mode, board)
            # bottom
            count2 = State.count_helper(seg, 0, -1, mode, board)
            result[mode.value-1][0] = count1 + count2

            # up right
            count1 = State.count_helper(seg, 1, 1, mode, board)
            # bottom left
            count2 = State.count_helper(seg, -1, -1, mode, board)
            result[mode.value-1][1] = count1 + count2

            # right
            count1 = State.count_helper(seg, 1, 0, mode, board)
            # left
            count2 = State.count_helper(seg, -1, 0, mode, board)
            result[mode.value-1][2] = count1 + count2

            # bottom right
            count1 = State.count_helper(seg, 1, -1, mode, board)
            # top left
            count2 = State.count_helper(seg, -1, 1, mode, board)
            result[mode.value-1][3] = count1 + count2

        return result

    @staticmethod
    def count_helper(seg, increment_x, increment_y, mode, board):
        x = seg.x
        y = seg.y
        next_x = x + increment_x
        next_y = y + increment_y

        if 0 <= next_x < Game.Game.max_x and 0 <= next_y < Game.Game.max_y:
            next_seg = board[next_y][next_x]
            if not isinstance(next_seg, CardSegment):
                return 0
            if (mode == Game.Choice.COLOR and next_seg.color == seg.color) or (
                    mode == Game.Choice.DOT and next_seg.dot == seg.dot):
                count = State.count_helper(next_seg, increment_x, increment_y, mode, board) + 1
            else:
                return 0
        else:
            return 0

        return count


def main():
    # print('''
    # ===============================
    # Regular Play: full first row
    # ===============================
    #         ''')

    # game = Game.Game(Game.Choice.COLOR)
    # game.place_card(1, 0, 0)
    # game.place_card(1, 2, 0)
    # game.place_card(1, 4, 0)
    # is_valid, prev_card, step, win= game.place_card(1, 6, 0)
    # Game.Game.print_board(game.board)
    # state=State(None, game.board, 4, prev_card)
    # state.generate_children()
    #
    # for child in state.children:
    #     Game.print_board(child.board)

    # print('''
    # ===============================
    # Regular Play: empty first row
    # ===============================
    #         ''')
    #
    # game = Game(Choice.COLOR)
    # Game.print_board(game.board)
    # state=State(None, game.board, 0, None)
    # state.generate_children()
    #
    # for child in state.children:
    #     Game.print_board(child.board)

    # print('''
    # ===============================
    # Regular Play: uneven last row
    # ===============================
    #         ''')
    #
    # game = Game.Game(Game.Choice.COLOR)
    # game.place_card(1, 0, 0)
    # game.place_card(1, 2, 0)
    # game.place_card(1, 4, 0)
    # game.place_card(1, 6, 0)
    # game.place_card(2, 0, 1)
    # game.place_card(1, 2, 1)
    # is_valid, prev_card, step, win = game.place_card(1, 4, 1)
    # Game.Game.print_board(game.board)
    # state = State(None, game.board, 4, prev_card)
    # state.generate_children()
    #
    # for child in state.children:
    #     Game.Game.print_board(child.board)

    # print('''
    # ===============================
    # Recycle Play: uneven last row
    # ===============================
    #         ''')
    #
    # game = Game.Game(Game.Choice.COLOR)
    # game.place_card(1, 0, 0)
    # game.place_card(1, 2, 0)
    # game.place_card(1, 4, 0)
    # game.place_card(1, 6, 0)
    # game.place_card(2, 0, 1)
    # game.place_card(1, 2, 1)
    # is_valid, prev_card, step, win = game.place_card(1, 4, 1)
    # Game.Game.print_board(game.board)
    # state = State(None, game.board, 4, prev_card)
    # state.generate_children()
    #
    # # for child in state.children:
    # #     Game.Game.print_board(child.board)

    # print('''
    # ===============================
    # Recycle Play: empty column
    # ===============================
    #         ''')
    #
    # game = Game.Game(Game.Choice.COLOR)
    # game.place_card(1, 2, 0)
    # game.place_card(1, 4, 0)
    # game.place_card(1, 6, 0)
    # game.place_card(2, 0, 1)
    # game.place_card(1, 2, 1)
    # is_valid, prev_card, step, win = game.place_card(1, 4, 1)
    # Game.Game.print_board(game.board)
    # state = State(None, game.board, 7, prev_card)
    # state.generate_children()

    # for child in state.children:
    #     Game.Game.print_board(child.board)

    # print('''
    # ===============================
    # Recycle Play: full column
    # ===============================
    #         ''')
    #
    # game = Game.Game(Game.Choice.COLOR)
    # game.place_card(1, 0, 0)
    # game.place_card(3, 0, 1)
    # game.place_card(5, 0, 2)
    # game.place_card(7, 0, 3)
    # game.place_card(1, 0, 4)
    # game.place_card(3, 0, 5)
    # game.place_card(5, 0, 6)
    # game.place_card(7, 0, 7)
    # game.place_card(1, 0, 8)
    # game.place_card(3, 0, 9)
    # game.place_card(5, 0, 10)
    # game.place_card(7, 0, 11)
    # is_valid, prev_card, step, win = game.place_card(1, 2, 0)
    # Game.Game.print_board(game.board)
    # state = State(None, game.board, 24, prev_card)
    # state.generate_children()
    #
    # for child in state.children:
    #     Game.Game.print_board(child.board)
    #     print(str(child.orig_x)+"; "+str(child.orig_y))

    # print('''
    # ===============================
    # Regular Play: Heuristic
    # ===============================
    #         ''')
    #
    # game = Game.Game(Game.Choice.COLOR)
    # game.place_card(3, 0, 0)
    # game.place_card(8, 2, 0)
    # game.place_card(8, 3, 0)
    # game.place_card(3, 4, 0)
    # game.place_card(3, 4, 1)
    # # game.place_card(1, 4, 1)
    # game.place_card(5, 0, 1)
    # game.place_card(4, 2, 2)
    # game.place_card(4, 3, 2)
    #
    # is_valid, prev_card, step, win = game.place_card(1, 4, 2)
    # # is_valid, prev_card, step, win = game.place_card(2, 0, 2)
    # Game.Game.print_board(game.board)
    # state = State(None, game.board, 9, prev_card)
    #
    # print(str(state.get_Heuristic()))

    print('''
    ===============================
    Heuristic
    ===============================
            ''')

    game = Game.Game(Game.Choice.COLOR)
    game.place_card(2, 0, 0)
    game.place_card(6, 1, 0)
    # game.place_card(2, 2, 0)
    # game.place_card(8, 2, 0)
    # is_valid, prev_card, step, win = game.place_card(1, 0, 2)
    is_valid, prev_card, step, win = game.place_card(2, 2, 0)
    Game.Game.print_board(game.board)
    state = State(None, game.board, 4, prev_card)
    state.generate_children()

    min_list=[float('inf')]*len(state.children)
    min_state=[None]*len(state.children)

    max = float('-inf')
    max_state = None

    for i in range(len(state.children)):
        e=state.children[i]
        e.generate_children()
        for c in e.children:
            h=c.get_H(Game.Choice.COLOR)
            if h<min_list[i]:
                min_list[i] = h
                min_state[i] = c
        if min_list[i]>max:
            max=min_list[i]
            max_state=min_state[i]

    Game.Game.print_board(max_state.board)
    print(max)
    Game.Game.print_board(max_state.parent.board)
    print(min_list)



    # game = Game.Game(Game.Choice.COLOR)
    # game.place_card(2, 0, 0)
    # game.place_card(2, 1, 0)
    # game.place_card(8, 2, 0)
    # is_valid, prev_card, step, win = game.place_card(8, 3, 0)
    # Game.Game.print_board(game.board)
    # state = State(None, game.board, 4, prev_card)
    # print(state.get_H(Game.Choice.COLOR))


if __name__ == '__main__':
    main()


