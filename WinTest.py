import numpy as np
import sys
# from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
# from PyQt5.QtGui import QIcon
# from PyQt5.QtCore import pyqtSlot
#
#
# class App(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.title = 'PyQt5 table - pythonspot.com'
#         self.left = 0
#         self.top = 0
#         self.width = 300
#         self.height = 200
#         self.initUI()
#
#     def initUI(self):
#         self.setWindowTitle(self.title)
#         self.setGeometry(self.left, self.top, self.width, self.height)
#
#         self.createTable()
#
#         # Add box layout, add table to box layout and add box layout to widget
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.tableWidget)
#         self.setLayout(self.layout)
#
#         # Show widget
#         self.show()
#
#     def createTable(self):
#         # Create table
#         self.tableWidget = QTableWidget()
#         self.tableWidget.setRowCount(12)
#         self.tableWidget.setColumnCount(8)
#         # self.tableWidget.setColumnWidth(30)
#         # self.tableWidget.setColumnWidth(1, 160)
#         self.tableWidget.setHorizontalHeaderLabels(('A', 'B', 'C','D', 'E', 'F','G', 'H'))
#         # self.tableWidget.setItem(0, 0, QTableWidgetItem("Cell (1,1)"))
#         # self.tableWidget.setItem(0, 1, QTableWidgetItem("Cell (1,2)"))
#         # self.tableWidget.setItem(1, 0, QTableWidgetItem("Cell (2,1)"))
#         # self.tableWidget.setItem(1, 1, QTableWidgetItem("Cell (2,2)"))
#         # self.tableWidget.setItem(2, 0, QTableWidgetItem("Cell (3,1)"))
#         # self.tableWidget.setItem(2, 1, QTableWidgetItem("Cell (3,2)"))
#         # self.tableWidget.setItem(3, 0, QTableWidgetItem("Cell (4,1)"))
#         # self.tableWidget.setItem(3, 1, QTableWidgetItem("Cell (4,2)"))
#         self.tableWidget.move(0, 0)
#
#         # table selection change
#         self.tableWidget.doubleClicked.connect(self.on_click)
#
#     @pyqtSlot()
#     def on_click(self):
#         print("\n")
#         for currentQTableWidgetItem in self.tableWidget.selectedItems():
#             print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())




test = np.zeros((12, 8))
test[0][0]=2
test[0][1]=3
test[0][2]=4
test[0][3]=2
test[0][3]=2
test[0][5]=4
test[0][6]=1
test[1][2]=2
test[1][6]=3
test[1][1]=1
test[1][0]=3
test[2][0]=1
test[2][1]=2
test[2][2]=2
test[3][0]=2
print(test)

px1=0;
# px2=1;
py1=0;
# py2=0;

def bfs(py1,px1,py2,px2,type,direction1,direction2,test,count):
    if py2 < 0 or py2 > 11 or px2 < 0 or px2 > 7:
        return
    count = dfs(py1, px1, test[py1][px1], direction1, test, 0) + dfs(py1, px1, test[py1][px1], direction2, test, 0) - 1
    if count == 4:
        print("win")
    else:
        print(test[py1][px1])
        print(count)

#     if test[py][px] == test[py+1][px+1] or test[py][px] == test[py-1][px-1]:
#         if dfs(py, px, test[py][px], 5, test, 0) + dfs(py, px, test[py][px], 7, test, 0)-1 ==4:
#             return "win"
#


    # if test[py][px] == test[py + 1][px - 1]  or  test[py][px] == test[py - 1][px + 1]:
    #
    # if test[py][px] == test[py + 1][px]  or  test[py][px] == test[py - 1][px]:
    # if test[py][px] == test[py][px + 1]  or  test[py][px] == test[py][px - 1]:

def dfs(py, px, type, direction, test, result):
    if py<0 or py>11 or px<0 or px>7:
        return result
    if test[py][px] == type:
        result += 1
    else:
        return result

    if direction==1:
        py+=1;
    elif direction==2:
        py-=1;
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

    result=dfs(py, px, type, direction, test, result)
    return result


#
# count = dfs(py1, px1, test[py1][px1], 5, test, 0) + dfs(py1, px1, test[py1][px1], 7, test, 0) - 1
# count = dfs(py1, px1, test[py1][px1], 6, test, 0) + dfs(py1, px1, test[py1][px1], 8, test, 0) - 1
# if count == 4:
#    print("win")
# else:
#    print(test[py1][px1])
#    print(count)
bfs(py1,px1,py1+1,px1,type,1,2,test,0);
bfs(py1,px1,py1-1,px1,type,1,2,test,0);
bfs(py1,px1,py1,px1+1,type,3,4,test,0);
bfs(py1,px1,py1,px1-1,type,3,4,test,0);
bfs(py1,px1,py1+1,px1+1,type,5,7,test,0);
bfs(py1,px1,py1-1,px1+1,type,6,8,test,0);
bfs(py1,px1,py1-1,px1-1,type,5,7,test,0);
bfs(py1,px1,py1+1,px1-1,type,6,8,test,0);