import numpy as np
import sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import (QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QApplication, QTableWidget, QTableWidgetItem)
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Game import Game
from Game import Choice
from CardSegment import Color
from CardSegment import Dot

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 table'
        self.left = 0
        self.top = 0
        self.width = 2500
        self.height = 2500
        self.positionY = -1
        self.positionX = -1
        self.type = -1

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setStyleSheet('background-color: white')
        self.setGeometry(self.left, self.top, self.width, self.height)

        # mode = input('Auto mode or Manual mode (1-Auto, 2-Manual): ')
        #
        # if mode[0] == '1':
        #     auto_input_sequence = input('Human Player: play first or second? (1-First, 2-Second): ')
        #     auto_input_choice = input('Human Player: play color or dot? (1-Color, 2-Dot): ')
        # else:
        manual_input = input('Player 1: play color or dot? (1-Color, 2-Dot): ')

        if manual_input=='1':
            self.choice = Choice.COLOR
        else:
            self.choice = Choice.DOT

        font = QtGui.QFont()
        font.setPixelSize(50)
        font.setBold(True)

        self.textLable = QLabel()
        self.countLable = QLabel()
        self.invalidLable = QLabel()

        self.textLable.setFont(font)
        self.countLable.setFont(font)
        self.invalidLable.setFont(font)

        self.phase = 'Normal Phase'
        self.textLable.setText(self.phase)
        # self.countLable.setText("count: ")
        self.game = Game(self.choice)

        self.createTable()
        self.createButton()

        # Add box layout, add table to box layout and add box layout to widget
        self.tableLayout = QHBoxLayout()
        self.tableLayout.addWidget(self.tableWidget)

        self.lableLayout = QVBoxLayout()
        self.lableLayout.addWidget(self.textLable)
        self.lableLayout.addWidget(self.invalidLable)
        self.lableLayout.addWidget(self.countLable)


        self.buttonSide1Layout = QVBoxLayout()
        self.buttonSide1Layout.addWidget(self.button1)
        self.buttonSide1Layout.addWidget(self.button2)
        self.buttonSide1Layout.addWidget(self.button3)
        self.buttonSide1Layout.addWidget(self.button4)

        self.buttonSide2Layout = QVBoxLayout()
        self.buttonSide2Layout.addWidget(self.button5)
        self.buttonSide2Layout.addWidget(self.button6)
        self.buttonSide2Layout.addWidget(self.button7)
        self.buttonSide2Layout.addWidget(self.button8)

        self.AnglebuttonSideLayout = QVBoxLayout()
        self.AnglebuttonSideLayout.addWidget(self.RecycleButton)

        self.Operationlayout = QHBoxLayout()
        self.Operationlayout.addLayout(self.buttonSide1Layout)
        self.Operationlayout.addLayout(self.buttonSide2Layout)
        self.Operationlayout.addLayout(self.AnglebuttonSideLayout)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.tableLayout)
        self.layout.addLayout(self.lableLayout)
        self.layout.addLayout(self.Operationlayout)

        self.setLayout(self.layout)
        # Show widget
        self.show()


    def createTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(12)
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(('A', 'B', 'C','D', 'E', 'F','G', 'H'))
        self.tableWidget.setVerticalHeaderLabels(('12', '11', '10','9', '8', '7','6', '5','4','3','2','1'))
        self.tableWidget.horizontalHeader().setDefaultSectionSize(130)
        self.tableWidget.verticalHeader().setDefaultSectionSize(130)

        for i in range(self.tableWidget.columnCount()):
            for j in range(self.tableWidget.rowCount()):
                #self.tableWidget.setItem(j, i, QTableWidgetItem("      ●"))
                # self.tableWidget.setItem(j, i, QTableWidgetItem("       O"))
                self.tableWidget.setItem(j, i, QTableWidgetItem(""))
        self.tableWidget.move(0, 0)

        # table selection changec
        self.tableWidget.clicked.connect(self.table_on_click)
        # print("press")


    @pyqtSlot()
    def table_on_click(self):
        # print("click\n")
        # print(self.tableWidget.cle)
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            self.positionX = currentQTableWidgetItem.column()
            self.positionY = currentQTableWidgetItem.row()
            print(12-self.positionY, str(chr(65+self.positionX)))
        if self.tableWidget.currentItem().text() != "":
            #    call method return the other segment
            card = self.game.get_card( self.positionX, 11-self.positionY)
            self.recylePosition1 = [card.seg[0].x,card.seg[0].y,card.seg[1].x,card.seg[1].y]
            print(card.seg[0].x,card.seg[0].y,card.seg[1].x,card.seg[1].y)
            self.tableWidget.setRangeSelected(
                #    select the whole card
                QTableWidgetSelectionRange(11-card.seg[0].y, card.seg[0].x, 11-card.seg[1].y, card.seg[1].x),True)

    def createButton(self):

        self.button1 = QPushButton('', self)
        self.button1.isFlat()
        self.button1.setStyleSheet('background: transparent')
        # self.button1.setAttribute(Qt.WA_TranslucentBackground, True)
        self.button1.setIcon(QtGui.QIcon('Type1.png'))
        self.button1.setIconSize(QtCore.QSize(300, 200))
        self.button1.clicked.connect(lambda *args: self.buttonType_on_click(1))

        self.button2 = QPushButton('', self)
        self.button2.isFlat()
        self.button2.setStyleSheet('background: transparent')
        self.button2.setIcon(QtGui.QIcon('Type2.png'))
        self.button2.setIconSize(QtCore.QSize(200, 200))
        self.button2.clicked.connect(lambda *args: self.buttonType_on_click(2))

        self.button3 = QPushButton('', self)
        self.button3.isFlat()
        self.button3.setStyleSheet('background: transparent')
        self.button3.setIcon(QtGui.QIcon('Type3.png'))
        self.button3.setIconSize(QtCore.QSize(300, 200))
        self.button3.clicked.connect(lambda *args: self.buttonType_on_click(3))

        self.button4 = QPushButton('', self)
        self.button4.isFlat()
        self.button4.setStyleSheet('background: transparent')
        self.button4.setIcon(QtGui.QIcon('Type4.png'))
        self.button4.setIconSize(QtCore.QSize(200, 200))
        self.button4.clicked.connect(lambda *args: self.buttonType_on_click(4))

        self.button5 = QPushButton('', self)
        self.button5.isFlat()
        self.button5.setStyleSheet('background: transparent')
        self.button5.setIcon(QtGui.QIcon('Type5.png'))
        self.button5.setIconSize(QtCore.QSize(300, 200))
        self.button5.clicked.connect(lambda *args: self.buttonType_on_click(5))

        self.button6 = QPushButton('', self)
        self.button6.isFlat()
        self.button6.setStyleSheet('background: transparent')
        self.button6.setIcon(QtGui.QIcon('Type6.png'))
        self.button6.setIconSize(QtCore.QSize(200, 200))
        self.button6.clicked.connect(lambda *args: self.buttonType_on_click(6))

        self.button7 = QPushButton('', self)
        self.button7.isFlat()
        self.button7.setStyleSheet('background: transparent')
        self.button7.setIcon(QtGui.QIcon('Type7.png'))
        self.button7.setIconSize(QtCore.QSize(300, 200))
        self.button7.clicked.connect(lambda *args: self.buttonType_on_click(7))

        self.button8 = QPushButton('', self)
        self.button8.isFlat()
        self.button8.setStyleSheet('background: transparent')
        self.button8.setIcon(QtGui.QIcon('Type8.png'))
        self.button8.setIconSize(QtCore.QSize(200, 200))
        self.button8.clicked.connect(lambda *args: self.buttonType_on_click(8))

        self.RecycleButton = QPushButton('', self)
        self.RecycleButton.isFlat()
        self.RecycleButton.setStyleSheet('background: transparent')
        self.RecycleButton.setIcon(QtGui.QIcon('Recyle.jpg'))
        self.RecycleButton.setIconSize(QtCore.QSize(200, 200))
        self.RecycleButton.clicked.connect(self.RecycleButton_on_click)
        # self.button1.setToolTip('This is an example button')
        # self.button.move(2300, 200)


    @pyqtSlot() #send the input to game
    def RecycleButton_on_click(self):
        is_valid, card_removed, card_added, count, win_id = self.game.recycle_card(
            self.recylePosition1[0],
            self.recylePosition1[1],
            self.recylePosition1[2],
            self.recylePosition1[3],
            self.type,
            self.positionX,
            11 - self.positionY
        )
        # print(is_valid, card_removed, card_added, count, win_id)
        if is_valid:
            self.invalidLable.setText("")
            self.tableWidget.setItem(
                11-card_removed.seg[0].y,card_removed.seg[0].x,
                QTableWidgetItem("")
            )
            self.tableWidget.item(
                11 - card_removed.seg[0].y, card_removed.seg[0].x,
            ).setBackground(QtGui.QColor(255, 255, 255))

            self.tableWidget.setItem(
                11 - card_removed.seg[1].y, card_removed.seg[1].x,
                QTableWidgetItem("")
            )
            self.tableWidget.item(
                11 - card_removed.seg[1].y, card_removed.seg[1].x,
            ).setBackground(QtGui.QColor(255, 255, 255))

            new_dot0, new_color0 = self.recycleHelper(card_added.seg[0])
            new_dot1, new_color1 = self.recycleHelper(card_added.seg[1])

            self.tableWidget.clearSelection()
            self.tableWidget.setItem(
                11 - card_added.seg[0].y, card_added.seg[0].x,
                QTableWidgetItem(new_dot0)
            )
            self.tableWidget.item(
                11 - card_added.seg[0].y, card_added.seg[0].x,
            ).setBackground(QtGui.QColor(new_color0[0],new_color0[1],new_color0[2]))

            self.tableWidget.setItem(
                11 - card_added.seg[1].y, card_added.seg[1].x,
                QTableWidgetItem(new_dot1)
            )
            self.tableWidget.item(
                11 - card_added.seg[1].y, card_added.seg[1].x,
            ).setBackground(QtGui.QColor(new_color1[0], new_color1[1], new_color1[2]))
        else:
            self.invalidLable.setText("Invalid Move")
        if win_id != 0 or count == 60:
            self.textLable.setText("Game End!")


    @pyqtSlot()
    def buttonType_on_click(self,buttonNum):
        self.type = buttonNum
        ShowY = 12 - self.positionY
        ShowX = str(chr(65 + self.positionX))
        if self.phase == 'Normal Phase':
            print(self.positionX, ShowY - 1, self.type)
            is_valid, card, count, win_id = self.game.place_card(self.type, self.positionX, ShowY - 1)
            print(is_valid, card, count, win_id)
            self.tableWidget.clearSelection()
            if is_valid:
                self.countLable.setText("count: "+str(count))
                self.invalidLable.setText("")
                if buttonNum == 1:
                    self.tableWidget.setItem(self.positionY, self.positionX, QTableWidgetItem("      ●"))
                    self.tableWidget.setItem(self.positionY, self.positionX + 1, QTableWidgetItem("      O"))
                    self.tableWidget.item(self.positionY, self.positionX).setBackground(QtGui.QColor(255, 0, 0))
                    self.tableWidget.item(self.positionY, self.positionX + 1).setBackground(QtGui.QColor(225, 225, 225))
                elif buttonNum == 2:
                    self.tableWidget.setItem(self.positionY - 1, self.positionX, QTableWidgetItem("      ●"))
                    self.tableWidget.setItem(self.positionY, self.positionX, QTableWidgetItem("      O"))
                    self.tableWidget.item(self.positionY, self.positionX).setBackground(QtGui.QColor(225, 225, 225))
                    self.tableWidget.item(self.positionY - 1, self.positionX).setBackground(QtGui.QColor(255, 0, 0))
                elif buttonNum == 3:
                    self.tableWidget.setItem(self.positionY, self.positionX, QTableWidgetItem("      O"))
                    self.tableWidget.setItem(self.positionY, self.positionX + 1, QTableWidgetItem("      ●"))
                    self.tableWidget.item(self.positionY, self.positionX).setBackground(QtGui.QColor(225, 225, 225))
                    self.tableWidget.item(self.positionY, self.positionX + 1).setBackground(QtGui.QColor(255, 0, 0))
                elif buttonNum == 4:
                    self.tableWidget.setItem(self.positionY, self.positionX, QTableWidgetItem("      ●"))
                    self.tableWidget.setItem(self.positionY - 1, self.positionX, QTableWidgetItem("      O"))
                    self.tableWidget.item(self.positionY, self.positionX).setBackground(QtGui.QColor(255, 0, 0))
                    self.tableWidget.item(self.positionY - 1, self.positionX).setBackground(QtGui.QColor(225, 225, 225))
                elif buttonNum == 5:
                    self.tableWidget.setItem(self.positionY, self.positionX, QTableWidgetItem("      O"))
                    self.tableWidget.setItem(self.positionY, self.positionX + 1, QTableWidgetItem("      ●"))
                    self.tableWidget.item(self.positionY, self.positionX).setBackground(QtGui.QColor(255, 0, 0))
                    self.tableWidget.item(self.positionY, self.positionX + 1).setBackground(QtGui.QColor(225, 225, 225))
                elif buttonNum == 6:
                    self.tableWidget.setItem(self.positionY, self.positionX, QTableWidgetItem("      ●"))
                    self.tableWidget.setItem(self.positionY - 1, self.positionX, QTableWidgetItem("      O"))
                    self.tableWidget.item(self.positionY - 1, self.positionX).setBackground(QtGui.QColor(255, 0, 0))
                    self.tableWidget.item(self.positionY, self.positionX).setBackground(QtGui.QColor(225, 225, 225))
                elif buttonNum == 7:
                    self.tableWidget.setItem(self.positionY, self.positionX, QTableWidgetItem("      ●"))
                    self.tableWidget.setItem(self.positionY, self.positionX + 1, QTableWidgetItem("      O"))
                    self.tableWidget.item(self.positionY, self.positionX).setBackground(QtGui.QColor(225, 225, 225))
                    self.tableWidget.item(self.positionY, self.positionX + 1).setBackground(QtGui.QColor(255, 0, 0))
                elif buttonNum == 8:
                    self.tableWidget.setItem(self.positionY - 1, self.positionX, QTableWidgetItem("      ●"))
                    self.tableWidget.setItem(self.positionY, self.positionX, QTableWidgetItem("      O"))
                    self.tableWidget.item(self.positionY, self.positionX).setBackground(QtGui.QColor(255, 0, 0))
                    self.tableWidget.item(self.positionY - 1, self.positionX).setBackground(QtGui.QColor(225, 225, 225))
            else:
                self.invalidLable.setText("Invalid Move")
            if count > 10:
                self.phase = 'Recyle Phase'
                self.textLable.setText(self.phase)
            if win_id != 0:
                self.textLable.setText("Game End!")

    def recycleHelper(self, seg):
        new_color = -1
        new_dot = -1
        if seg.color == Color.RED:
            new_color = [255, 0, 0]
        elif seg.color == Color.WHITE:
            new_color = [225, 225, 225]
        if seg.dot == Dot.SOLID:
            new_dot = "      ●"
        elif seg.dot == Dot.EMPTY:
            new_dot = "      O"
        return new_dot, new_color


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

