import numpy as np
from CardSegment import CardSegment
from CardSegment import Color
from CardSegment import Dot
# from Game import Game

class State:

    def __init__(self, parent, board, step, prev_card):
        """
        Ctor for State class
        :param parent: parent State, can be None for the root node
        :param board: based on which board create the board of current state
        :param step: the count of steps of the this State
        :param prev_card: the most recent card has been placed in the previous step
        """
        self.board = np.copy(board)
        self.step = step
        self.prev_card = prev_card
        self.parent = parent
        self.children = []
        self.highest_row = [-1] * 8

    def generate_children(self):
        """
        Generate children state for a state node and add it the current node's children list
        """
        # TODO: Implement state generation for recycle phase
        if self.step <= 24:
            self.generate_regular_move()

    def generate_regular_move(self):
        if self.highest_row[0] == -1:
            self.find_highest_row()

        for i in range(8):
            if self.highest_row[i] < 12:
                for t in range(1, 9):
                    new_board = np.copy(self.board)
                    # is_valid_play, win_list, prev_card = Game.play_normal(t, i, self.highest_row[i], new_board,
                    #                                                       self.prev_card, False)
                    # if is_valid_play:
                    state = State(self, new_board, self.step + 1, self.prev_card )
                    self.children.append(state)

    def find_highest_row(self):
        for j in range(8):
            for i in range(12):
                if not isinstance(self.board[i][j], CardSegment):
                    self.highest_row[j] = i
                    break
            if self.highest_row[j] == -1:
                self.highest_row[j] = i

    def get_Heuristic(self):
        sum = 0
        for j in range(8):
            for i in range(12):
                if isinstance(self.board[i][j], CardSegment):
                    coordinates_Val = i*10 + j -1
                    print(coordinates_Val)
                    if (self.board[i][j].color == Color.WHITE and self.board[i][j].dot == Dot.EMPTY):
                        sum += coordinates_Val
                    if (self.board[i][j].color == Color.WHITE and self.board[i][j].dot == Dot.SOLID):
                        sum += 3*coordinates_Val
                    if (self.board[i][j].color == Color.RED and self.board[i][j].dot == Dot.SOLID):
                        sum -= 2 * coordinates_Val
                    if (self.board[i][j].color == Color.RED and self.board[i][j].dot == Dot.EMPTY):
                        sum -= 1.5 * coordinates_Val

#
# def main():
#     # print('''
#     # ===============================
#     # Regular Play: full first row
#     # ===============================
#     #         ''')
#     #
#     # game = Game(Choice.COLOR)
#     # game.place_card(1, 0, 0)
#     # game.place_card(1, 2, 0)
#     # game.place_card(1, 4, 0)
#     # is_valid, prev_card, step, win= game.place_card(1, 6, 0)
#     # Game.print_board(game.board)
#     # state=State(None, game.board, 4, prev_card)
#     # state.generate_children()
#     #
#     # for child in state.children:
#     #     Game.print_board(child.board)
#
#     # print('''
#     # ===============================
#     # Regular Play: empty first row
#     # ===============================
#     #         ''')
#     #
#     # game = Game(Choice.COLOR)
#     # Game.print_board(game.board)
#     # state=State(None, game.board, 0, None)
#     # state.generate_children()
#     #
#     # for child in state.children:
#     #     Game.print_board(child.board)
#
#     print('''
#     ===============================
#     Regular Play: uneven last row
#     ===============================
#             ''')
#
#     game = Game(Choice.COLOR)
#     game.place_card(1, 0, 0)
#     game.place_card(1, 2, 0)
#     game.place_card(1, 4, 0)
#     game.place_card(1, 6, 0)
#     game.place_card(2, 0, 1)
#     game.place_card(1, 2, 1)
#     is_valid, prev_card, step, win= game.place_card(1, 4, 1)
#     Game.print_board(game.board)
#     state=State(None, game.board, 4, prev_card)
#     state.generate_children()
#
#     for child in state.children:
#         Game.print_board(child.board)
#
#
# if __name__ == '__main__':
#     main()