import Game_Tree
from TreeDriver import Node
from TreeDriver import Tree

class MiniMax:

    def __init__(self, game_tree, curChoice):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.root  # GameNode
        self.currentNode = None     # GameNode
        self.successors = []        # List of GameNodes
        self.curChoice = curChoice
        return

    def minimax(self, node):
        # first, find the max value
        if self.curChoice == "Choice.COLOR":
            best_val = self.max_value(node)
        else:
            best_val = self.min_value(node)
        successors = self.getSuccessors(node)
        # find the node with our best move
        best_move = None
        for elem in successors:
            if elem.val == best_val:
                best_move = elem
                break

        return best_move


    def max_value(self, node):
        if self.isTerminal(node):
            return self.getUtility(node)

        infinity = float('inf')
        max_value = -infinity

        successors_states = self.getSuccessors(node)
        for state in successors_states:
            max_value = max(max_value, self.min_value(state))
            state.val = self.min_value(state)

        return max_value


    def min_value(self, node):
        if self.isTerminal(node):
            return self.getUtility(node)

        infinity = float('inf')
        min_value = infinity

        successor_states = self.getSuccessors(node)
        for state in successor_states:
            min_value = min(min_value, self.max_value(state))
            state.val = self.max_value(state)

        return min_value


    # successor states in a game tree are the child nodes...
    def getSuccessors(self, node):
        return node.children

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isTerminal(self, node):
        return len(node.children) == 0

    def getUtility(self, node):
         # return node.val
         return node.get_Heuristic()

# def main():
#     root = Node(3)
#     node11 = Node(3)
#     node12 = Node(9)
#     node13 = Node(0)
#     node14 = Node(7)
#     node15 = Node(12)
#     node16 = Node(6)
#
#     node11.addChildren(Node(2))
#     node11.addChildren(Node(3))
#
#     node12.addChildren(Node(5))
#     node12.addChildren(Node(9))
#
#     node13.addChildren(Node(0))
#     node13.addChildren(Node(-1))
#
#     node14.addChildren(Node(7))
#     node14.addChildren(Node(4))
#
#     node15.addChildren(Node(2))
#     node15.addChildren(Node(1))
#
#     node16.addChildren(Node(5))
#     node16.addChildren(Node(6))
#
#     node21 = Node(21)
#     node22 = Node(22)
#     node23 = Node(23)
#
#     node21.addChildren(node11)
#     node21.addChildren(node12)
#
#     node22.addChildren(node13)
#     node22.addChildren(node14)
#
#     node23.addChildren(node15)
#     node23.addChildren(node16)
#
#
#     root.addChildren(node21)
#     root.addChildren(node22)
#     root.addChildren(node23)
#
#     tree=Tree(root)
#     tree.printTree(root,1)
#     cur = "Choice.DOT"
#     alpha = MiniMax(tree, cur)
#     best = alpha.minimax(root)
#     tree.printTree(root, 1)
#     print(best.val)
#
# if __name__ == '__main__':
#     main()