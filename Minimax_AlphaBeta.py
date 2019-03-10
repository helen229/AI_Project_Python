
import Game_Tree
# from TreeDriver import Node
# from TreeDriver import Tree

class AlphaBeta:

    def __init__(self, game_tree, curChoice):
        self.game_tree = game_tree  # GameTree
        self.root = game_tree.root  # GameNode
        self.curChoice = curChoice
        self.countH = 0

    def alpha_beta_search(self, node):
        infinity = float('inf')

        if self.curChoice == "Choice.COLOR":
            best_val = -infinity
            beta = infinity

            childrenNodeList = self.getChildren(node)
            best_state = None
            for state in childrenNodeList:
                value = self.min_value(state, best_val, beta)
                state.val = value
                if value > best_val:
                    best_val = value
                    best_state = state
        else:
            best_val = infinity
            alpha = -infinity

            childrenNodeList = self.getChildren(node)
            best_state = None
            for state in childrenNodeList:
                value = self.max_value(state, alpha, best_val)
                state.val = value
                if value < best_val:
                    best_val = value
                    best_state = state
        return best_state

    def max_value(self, node, alpha, beta):

        if self.isLeaf(node):
            self.countH += 1
            # node.val = self.getHeuristic(node)
            return self.getHeuristic(node)
        infinity = float('inf')
        value = -infinity

        childrenNodeList = self.getChildren(node)
        for state in childrenNodeList:
            value = max(value, self.min_value(state, alpha, beta))
            state.val = value
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value

    def min_value(self, node, alpha, beta):

        if self.isLeaf(node):
            self.countH +=1
            # node.val=self.getHeuristic(node)
            return self.getHeuristic(node)
        infinity = float('inf')
        value = infinity

        childrenNode = self.getChildren(node)
        for state in childrenNode:
            value = min(value, self.max_value(state, alpha, beta))
            state.val = value
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value


    # successor states in a game tree are the child nodes...
    def getChildren(self, node):
        return node.children

    # return true if the node has NO children (successor states)
    # return false if the node has children (successor states)
    def isLeaf(self, node):
        return len(node.children) == 0

    def getHeuristic(self, node):
        # return node.val
        return node.get_Heuristic()
#
def main():
    root = Node(3)
    node11 = Node(3)
    node12 = Node(9)
    node13 = Node(0)
    node14 = Node(7)
    node15 = Node(12)
    node16 = Node(6)

    node11.addChildren(Node(2))
    node11.addChildren(Node(3))

    node12.addChildren(Node(5))
    node12.addChildren(Node(9))

    node13.addChildren(Node(0))
    node13.addChildren(Node(-1))

    node14.addChildren(Node(7))
    node14.addChildren(Node(4))

    node15.addChildren(Node(2))
    node15.addChildren(Node(1))

    node16.addChildren(Node(3))
    node16.addChildren(Node(6))

    node21 = Node(3)
    node22 = Node(0)
    node23 = Node(22)

    node21.addChildren(node11)
    node21.addChildren(node12)

    node22.addChildren(node13)
    node22.addChildren(node14)

    node23.addChildren(node15)
    node23.addChildren(node16)

    root.addChildren(node21)
    root.addChildren(node22)
    root.addChildren(node23)

    tree=Tree(root)
    tree.printTree(root)
    cur = "Choice.COLOR"
    alpha = AlphaBeta(tree, cur)

    best = alpha.alpha_beta_search(root)
    tree.printTree(root)
    print(best.val)

if __name__ == '__main__':
    main()