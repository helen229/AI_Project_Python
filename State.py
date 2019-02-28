import numpy as np


class State:

    def __init__(self, parent, old_board, old_step, prev_card):
        """
        Ctor for State class
        :param parent: parent State, can be None for the root node
        :param old_board: based on which board create the board of current state, usually should be parent.board
        :param old_step: the count of steps of the previous move
        :param prev_card: the most recent card has been placed in the previous step
        """
        self.board = np.copy(old_board)
        self.step = old_step + 1
        self.prev_card = prev_card
        self.parent = parent
        self.children = []

    def add_child(self, child):
        """
        Add a child or children list to current State node
        :param child: A single State object or a list of State objects
        """
        self.children.append(child)
