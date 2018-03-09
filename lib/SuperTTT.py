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
    dead = False
    winner = None

    def __init__(self, *args, **kwargs):
        super(MyButton, self).__init__(*args, **kwargs)

    def set_marked(self, mark):
        self.marked = mark

    def get_marked(self):
        mark = self.marked
        return mark

    def set_dead(self):
        self.dead = True

    def get_dead(self):
        dead = self.dead
        return dead

    def set_winner(self, win):
        self.winner = win
        if win == 0:
            self.set_dead()

    def get_winner(self):
        win = self.winner
        return win


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
        self.parent.inwinner_sign.emit(randint(0, 2))
        self.close_round()

    def end_time(self):
        delta = datetime.datetime.now() - self.begin
        if not delta.second < 135:
            print 'END TIME!!'
            self.close_round()

    def close_round(self):
        self.parent.activateWindow()
        self.close()
        self.parent.check_sign.emit()

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
    last_marked = None
    inwinner_sign = QtCore.pyqtSignal(int)
    winner_sign = QtCore.pyqtSignal(list)
    check_sign = QtCore.pyqtSignal()

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
        self.inwinner_sign[int].connect(self.winner_round)
        self.winner_sign[list].connect(self.winner_game)
        self.check_sign.connect(self.verify_winner)

    def play_house(self):
        # PLAYS THE INSIDER TICTACTOE IF BUTTON NOT CHECKED
        btn = self.sender()
        if isinstance(btn, MyButton):
            if not self.verify_active_round() and not btn.get_marked():
                self.last_marked = btn
                btn.set_marked(True)
                self.tictactoe = TicTacToe(self)
                self.tictactoe.create_ui()

    def verify_active_round(self):
        round = [r for r in self.children() if isinstance(r, TicTacToe)]
        marks = [b for b in self.buttons if b.get_marked()]
        if len(round) == len(marks):
            return False
        else:
            return True

    def winner_round(self, value):
        btn = self.last_marked
        btn.set_winner(value)
        if value == 1:
            btn.setIcon(QtGui.QIcon(__CROSSPATH__))
        elif value == 2:
            btn.setIcon(QtGui.QIcon(__CIRCLEPATH__))
        else:
            btn.setIcon(QtGui.QIcon(__DEADPATH__))

    def winner_game(self, buttons):
        for i in xrange(10):
            for btn in buttons:
                self.buttons[btn].setStyleSheet(
                    "background-color: rgb(214,183,255)")
            for btn in buttons:
                self.buttons[btn].setStyleSheet(
                    "background-color: rgb(183,255,225)")

    def verify_winner(self):
        rows = [[j + i * 3 for j in xrange(3)] for i in xrange(3)]
        cols = [[i + j * 3 for j in xrange(3)] for i in xrange(3)]
        diags = [[0, 4, 8], [2, 4, 6]]
        all_wins = [rows, cols, diags]

        def winner(win):
            for i in xrange(2):
                if win[i] != win[i + 1]:
                    return False
            return True

        for aw in all_wins:
            for w in aw:
                win = [self.buttons[btn].get_winner() for btn in w]
                dead = [btn for btn in w if
                        self.buttons[btn].get_dead() or not self.buttons[btn].get_winner()]
                if len(dead) != 0:
                    pass
                elif winner(win):
                    print win
                    self.winner_sign.emit(win)
