class State:
    def __init__(self, parent, old_board, old_step, prev_card):
        self.board=old_board
        self.step=old_step+1
        self.prev_card=prev_card
        self.parent=parent
        self.children=[]

    def add_child(self, child):
        self.children.append(child)
