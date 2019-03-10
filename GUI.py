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
        self.width = 2700
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
        self.mode = '1'

        if self.mode == '1':
            self.auto_input_alg = input('alpha-beta should be activated or not? (1-YES, 2-NO just Mini Max): ')
            # auto_input_file = input('should generate a trace of the minimax / alpha-beta or not? (1-YES, 2-NO): ')
            auto_input_sequence = input('Computer Player: play first or second? (1-First, 2-Second): ')

            # auto mode
            if auto_input_sequence == '2':
                self.curPlayer = "Human Player"
            else:
                self.curPlayer = "Computer Player"

            auto_input_choice = input(self.curPlayer+': play color or dot? (1-Color, 2-Dot): ')

            if auto_input_choice == '1':
                self.choice = Choice.COLOR
            elif auto_input_choice == '2':
                self.choice = Choice.DOT
            # if auto_input_choice == '1' and auto_input_sequence == '1':
            #     self.choice = Choice.COLOR
            # elif auto_input_choice == '2' and auto_input_sequence == '2':
            #     self.choice = Choice.DOT
            # elif auto_input_choice == '2' and auto_input_sequence == '1':
            #     self.choice = Choice.DOT
            # elif auto_input_choice == '2' and auto_input_sequence == '2':
            #     self.choice = Choice.COLOR

        else:
            manual_input = input('Player 1: play color or dot? (1-Color, 2-Dot): ')
            # manual mode
            self.curPlayer = "Player 1"
            if manual_input == '1':
                self.choice = Choice.COLOR
            else:
                self.choice = Choice.DOT



        font = QtGui.QFont()
        font.setPixelSize(50)
        font.setBold(True)

        smallfont = QtGui.QFont()
        smallfont.setPixelSize(40)

        self.textLable = QLabel()
        self.countLable = QLabel()
        self.invalidLable = QLabel()
        self.playerLable = QLabel()

        self.textLable.setFont(font)
        self.countLable.setFont(font)
        self.invalidLable.setFont(font)
        self.playerLable.setFont(smallfont)

        self.phase = 'Normal Phase'
        self.textLable.setText(self.phase)
        self.playerLable.setText(self.curPlayer+'('+str(self.choice)+')')

        self.game = Game(self.choice)

        self.createTable()
        self.createButton()

        self.editor = QtWidgets.QTextEdit()
        self.editor.setText("hello")

        # Add box layout, add table to box layout and add box layout to widget
        self.tableLayout = QHBoxLayout()
        self.tableLayout.addWidget(self.tableWidget)

        self.lableLayout = QVBoxLayout()
        self.lableLayout.addStretch(0.5)
        self.lableLayout.addWidget(self.textLable)
        self.lableLayout.addStretch(0.7)
        self.lableLayout.addWidget(self.playerLable)
        self.lableLayout.addStretch(0.7)
        self.lableLayout.addWidget(self.countLable)
        self.lableLayout.addStretch(0.7)
        self.lableLayout.addWidget(self.invalidLable)
        self.lableLayout.addStretch(0.5)
        self.lableLayout.addWidget(self.editor)
        self.lableLayout.addStretch(0.6)
        self.lableLayout.addWidget(self.editor_button)

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
        self.AnglebuttonSideLayout.addWidget(self.computerPlayerButton)

        self.Operationlayout = QHBoxLayout()
        self.Operationlayout.addStretch(1)
        self.Operationlayout.addLayout(self.lableLayout)
        self.Operationlayout.addStretch(1)
        self.Operationlayout.addLayout(self.buttonSide1Layout)
        self.Operationlayout.addStretch(1)
        self.Operationlayout.addLayout(self.buttonSide2Layout)
        self.Operationlayout.addStretch(1)
        self.Operationlayout.addLayout(self.AnglebuttonSideLayout)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.tableLayout)
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
                self.tableWidget.setItem(j, i, QTableWidgetItem(""))
        self.tableWidget.move(0, 0)

        # table selection change
        self.tableWidget.clicked.connect(self.table_on_click)


    @pyqtSlot()
    def table_on_click(self):
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
        self.button2 = QPushButton('', self)
        self.button3 = QPushButton('', self)
        self.button4 = QPushButton('', self)
        self.button5 = QPushButton('', self)
        self.button6 = QPushButton('', self)
        self.button7 = QPushButton('', self)
        self.button8 = QPushButton('', self)

        self.createButtonHelper(self.button1, 'Type1.png', 300, 200, 1)
        self.createButtonHelper(self.button2, 'Type2.png', 200, 200, 2)
        self.createButtonHelper(self.button3, 'Type3.png', 300, 200, 3)
        self.createButtonHelper(self.button4, 'Type4.png', 200, 200, 4)

        self.createButtonHelper(self.button5, 'Type5.png', 300, 200, 5)
        self.createButtonHelper(self.button6, 'Type6.png', 200, 200, 6)
        self.createButtonHelper(self.button7, 'Type7.png', 300, 200, 7)
        self.createButtonHelper(self.button8, 'Type8.png', 200, 200, 8)

        self.editor_button = QPushButton('play', self)
        self.editor_button.clicked.connect(self.Editor_button_on_click)
        self.editor_button.setStyleSheet('background: transparent')
        self.editor_button.setIcon(QtGui.QIcon('Play_image.png'))
        self.editor_button.setIconSize(QtCore.QSize(100, 100))

        self.RecycleButton = QPushButton('', self)
        self.RecycleButton.isFlat()
        self.RecycleButton.setStyleSheet('background: transparent')
        self.RecycleButton.setIcon(QtGui.QIcon('Recyle.jpg'))
        self.RecycleButton.setIconSize(QtCore.QSize(200, 200))
        self.RecycleButton.clicked.connect(self.RecycleButton_on_click)

        self.computerPlayerButton = QPushButton('', self)
        self.computerPlayerButton.isFlat()
        self.computerPlayerButton.setStyleSheet('background: transparent')
        self.computerPlayerButton.setIcon(QtGui.QIcon('Play_image.png'))
        self.computerPlayerButton.setIconSize(QtCore.QSize(200, 200))
        self.computerPlayerButton.clicked.connect(self.computerPlayerButton_on_click)


    def createButtonHelper(self, button, icon, sizeY, sizeX, number):
        button.isFlat()
        button.setStyleSheet('background: transparent')
        button.setIcon(QtGui.QIcon(icon))
        button.setIconSize(QtCore.QSize(sizeY, sizeX))
        button.clicked.connect(lambda *args: self.buttonType_on_click(number))

    @pyqtSlot()  # send the input to game
    def Editor_button_on_click(self):
        print(self.editor.toPlainText())

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
            # remove previous card
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
            # add new card
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
        if win_id == 1:
            self.textLable.setText("Player1 Win!")
        if win_id == 2:
            self.textLable.setText("Player2 Win!")
        if count == 60:
            self.textLable.setText("Draw!")


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

    @pyqtSlot()  # computer move
    def computerPlayerButton_on_click(self):
        print("computer move")
        if self.curPlayer == "Computer Player":
            card_removed, card_added, count, win_id = self.game.computer_move(str(self.choice),self.auto_input_alg, True)

            new_dot0, new_color0 = self.recycleHelper(card_added.seg[0])
            new_dot1, new_color1 = self.recycleHelper(card_added.seg[1])

            self.countLable.setText("count: " + str(count))
            self.playerChange()
            self.playerLable.setText(self.curPlayer + '(' + str(self.choice) + ')')
            self.invalidLable.setText("")
            if count >23:
                self.phase = 'Recyle Phase'
            self.tableWidget.clearSelection()
            if card_removed != None:
                # remove previous card
                self.tableWidget.setItem(
                    11 - card_removed.seg[0].y, card_removed.seg[0].x,
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
            # add new card
            self.tableWidget.setItem(
                11 - card_added.seg[0].y, card_added.seg[0].x,
                QTableWidgetItem(new_dot0)
            )
            self.tableWidget.item(
                11 - card_added.seg[0].y, card_added.seg[0].x,
            ).setBackground(QtGui.QColor(new_color0[0], new_color0[1], new_color0[2]))

            self.tableWidget.setItem(
                11 - card_added.seg[1].y, card_added.seg[1].x,
                QTableWidgetItem(new_dot1)
            )
            self.tableWidget.item(
                11 - card_added.seg[1].y, card_added.seg[1].x,
            ).setBackground(QtGui.QColor(new_color1[0], new_color1[1], new_color1[2]))

            if win_id == 1:
                self.textLable.setText("Player1 Win!")
            if win_id == 2:
                self.textLable.setText("Player2 Win!")
            if count == 60:
                self.textLable.setText("Draw!")

        else:
            self.invalidLable.setText("Invalid Player")

    @pyqtSlot()
    def buttonType_on_click(self,buttonNum):
        self.type = buttonNum
        ShowY = 12 - self.positionY
        ShowX = str(chr(65 + self.positionX))
        if self.phase == 'Normal Phase':
            print(self.positionX, ShowY - 1, self.type)
            # auto mode Human player or manual mode
            if (self.mode == '1' and self.curPlayer == "Human Player") or self.mode == '2':
                is_valid, card, count, win_id = self.game.place_card(self.type, self.positionX, ShowY - 1)
                self.tableWidget.clearSelection()
                if is_valid:
                    self.countLable.setText("count: "+str(count))
                    self.playerChange()
                    self.playerLable.setText(self.curPlayer + '(' + str(self.choice) + ')')
                    self.invalidLable.setText("")
                    # paint the cells
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
                if count > 24:
                    self.phase = 'Recyle Phase'
                    self.textLable.setText(self.phase)
                if win_id == 1:
                    self.textLable.setText("Player1 Win!")
                if win_id == 2:
                    self.textLable.setText("Player2 Win!")
                if count == 60:
                    self.textLable.setText("Draw!")
            else:
                self.invalidLable.setText("Invalid Player")


    @pyqtSlot()
    def playerChange(self):
        if self.curPlayer == "Player 1":
            self.curPlayer = "Player 2"
        elif self.curPlayer == "Player 2":
            self.curPlayer = "Player 1"
        elif self.curPlayer == "Human Player":
            self.curPlayer = "Computer Player"
        elif self.curPlayer == "Computer Player":
            self.curPlayer = "Human Player"
        if self.choice == Choice.DOT:
            self.choice = Choice.COLOR
        elif self.choice == Choice.COLOR:
            self.choice = Choice.DOT



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

