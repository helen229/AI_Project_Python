# class Board:
#
#     def __init__(self, BoardNode):
#         self.boardNode = BoardNode
#         self.Children = []
#
#
#     def setChildren(self, childrenList):
#         self.Children.append(childrenList)
#
#
#     def getChildren(self):
#         return self.Children

import State

class Game_Tree:

    def __init__(self, root):
        self.root = root
        # self.countH = 0

    def getChildrenNode(self, rootBoard):
        return rootBoard.children

    def generateChildrenNode(self, rootBoard):

        rootBoard.generate_children()
        return rootBoard.children


    def generateTreeLayer(self, parentBoard):

        BoardList = parentBoard.getChildren()
        for node in BoardList:
            node.setChildren(self.generateChildrenNode(node))


    def generateNLayerTree(self, rootBoard, n):
        self.generateChildrenNode(rootBoard)
        if self.getHeight(rootBoard) >= n:
            return
        else:
            boardOpenList = self.getChildrenNode(rootBoard)
            for node in boardOpenList:
                self.generateNLayerTree(node, n-1)


    #the distance between the node and leaf
    def getHeight(self, node):
        max_val = 0
        if self.isLeaf(node):
            return 0
        else:
            for child in node.children:
                node = child
                max(max_val,self.getHeight(node)+1)
        return max_val


    def isLeaf(self, node):
        return len(node.children) == 0

    def printTree(self, node):
        curr = [node]
        while curr:
            next_level = []
            for n in curr:
                print(n.val, end=' ')
                next_level.extend(n.children)
            print()
            print(len(next_level))
            curr = next_level