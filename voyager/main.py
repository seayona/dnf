import datetime
import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QBasicTimer, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget

from game import Player, Game
from recognition import Recogbot

VoyagerWindow, _ = uic.loadUiType("ui/main.ui")


# 【探索者】
class Voyager(QMainWindow, VoyagerWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.timer = QTimer()
        self.timer.timeout.connect(self._interval)

        self.game = Game()
        self.recogbot = Recogbot()
        self.player = Player()

        self.show()
        print("【探索者】启动成功")
        print("【探索者】按F8键启动/F12键停止/Esc键退出程序")

        self.startButton.clicked.connect(self.onStart)
        self.stopButton.clicked.connect(self.onStop)

    def onStart(self):
        print("【探索者】开启自动搬砖模式")
        self.timer.start(1000)
        self.player.attack()

    def onStop(self):
        print("【探索者】关闭自动搬砖模式")
        self.timer.stop()
        self.player.stand()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F8:
            self.onStart()
        if e.key() == Qt.Key_F12:
            self.onStop()
        if e.key() == Qt.Key_Escape:
            self.close()

    def _interval(self):
        # 释放觉醒
        if self.recogbot.boss():
            print("【目标检测】发现Boss!")
            self.player.finisher()

        # 释放技能
        if self.recogbot.loveyAlive():
            print("【目标检测】还有小可爱活着")
            self.player.cast()

        # 战斗奖励
        if self.recogbot.reward():
            print("【目标检测】战斗奖励，战斗结束!")
            self.game.reward()

        if self.recogbot.bag():
             self.game.repair()

        if self.recogbot.replay():
            self.game.replay()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    voyager = Voyager()
    sys.exit(app.exec_())
