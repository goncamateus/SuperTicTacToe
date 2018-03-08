import sys
import os
import time
import datetime
from random import randint
from PyQt4 import QtGui, QtCore

__ICONPATH__ = os.path.join(os.path.abspath('.'), 'resources/icon.png')
__CROSSPATH__ = os.path.join(os.path.abspath('.'), 'resources/cross.png')
__CIRCLEPATH__ = os.path.join(os.path.abspath('.'), 'resources/circle.png')
__DEADPATH__ = os.path.join(os.path.abspath('.'), 'resources/dead.png')


class MyButton(QtGui.QPushButton):

    marked = False

    def __init__(self, *args, **kwargs):
        super(MyButton, self).__init__(*args, **kwargs)

    def set_marked(self, mark):
        self.marked = mark

    def get_marked(self):
        mark = self.marked
        return mark


class TicTacToe(QtGui.QMainWindow):

    buttons = None
    actual_player = None
    button_icon = None
    begin = None

    def __init__(self, parent=None):
        super(TicTacToe, self).__init__(parent)
        self.setGeometry(parent.geometry())
        self.setWindowTitle('Match')
        self.setFixedSize(270, 270)
        
        self.buttons = [MyButton('', self) for i in xrange(9)]
        self.actual_player = 0
        self.parent = parent
        self.parent.showMinimized()

    def create_ui(self):
        for j in range(3):
            btns = self.buttons[j * 3:(j + 1) * 3]
            for i, btn in enumerate(btns):
                btn.resize(90, 90)
                btn.move(90 * i, 90 * j)
                btn.setIconSize(QtCore.QSize(90, 90))
        for i, btn in enumerate(self.buttons):
            btn.clicked.connect(self.set_button_icon)
        self.connect(self, QtCore.SIGNAL('triggered()'), self.closeEvent)
        self.show()
        self.begin = datetime.datetime.now()
        self.tictactoe()

    def tictactoe(self):
        rand = randint(1, 2)
        if rand == 1:
            self.setWindowTitle('Player 1')
        else:
            self.setWindowTitle('Player 2')

        # while(not self.win()):
        if self.actual_player == 0:
            self.button_icon = __CROSSPATH__
        else:
            self.button_icon = __CIRCLEPATH__

    def win(self):
        self.parent.winner_sign.emit(str(randint(1, 2)))
        self.close_round()

    def end_time(self):
        delta = datetime.datetime.now() - self.begin
        if not delta.second < 135:
            print 'END TIME!!'
            self.close_round()

    def close_round(self):
        self.parent.activateWindow()
        self.close()

    def closeEvent(self, event):
        self.close_round()

    def set_button_icon(self):
        btn = self.sender()
        if isinstance(btn, MyButton):
            btn.setIcon(QtGui.QIcon(self.button_icon))
            self.win()


class SuperTicTacToe(QtGui.QMainWindow):

    buttons = None
    tictactoe = None
    round_winner = None
    winner_sign = QtCore.pyqtSignal(str)
    bubu = QtCore.pyqtSignal(int)

    def __init__(self):
        super(SuperTicTacToe, self).__init__()
        self.setGeometry(50, 50, 270, 270)
        self.setWindowTitle('Super Tic Tac Toe')
        self.setWindowIcon(QtGui.QIcon(__ICONPATH__))
        self.setFixedSize(270, 270)
        self.buttons = [MyButton('', self) for i in xrange(9)]
        self.super_tic_tac_toe()
        self.show()

    def super_tic_tac_toe(self):
        for j in range(3):
            btns = self.buttons[j * 3:(j + 1) * 3]
            for i, btn in enumerate(btns):
                btn.resize(90, 90)
                btn.move(90 * i, 90 * j)
                btn.setIconSize(QtCore.QSize(90, 90))
        for i, btn in enumerate(self.buttons):
            btn.clicked.connect(self.play_house)
        self.winner_sign[str].connect(self.winner_round)

    def play_house(self):
        # PLAYS THE INSIDER TICTACTOE IF BUTTON NOT CHECKED
        btn = self.sender()
        if isinstance(btn, MyButton):
            if not self.verify_active_round(btn) and not btn.get_marked():
                btn.set_marked(True)
                self.tictactoe = TicTacToe(self)
                self.tictactoe.create_ui()

    def verify_active_round(self, button):
        round = [r for r in self.children() if isinstance(r,TicTacToe)]
        if len(round) == 0:
            return False
        else:
            return True

    def winner_round(self, value):
        for btn in self.buttons:
            if btn.icon().name() == '' and btn.get_marked():
                if int(value) == 1:
                    btn.setIcon(QtGui.QIcon(__CROSSPATH__))
                else:
                    btn.setIcon(QtGui.QIcon(__CIRCLEPATH__))
