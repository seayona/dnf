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
        self.timer.timeout.connect(self.onInterval)

        self.game = Game()
        self.recogbot = Recogbot()
        self.player = Player()

        self.show()
        print("【探索者】启动成功")
        print("【探索者】按F8键启动/F12键停止/Esc键退出程序")

    def onStart(self):
        print("【探索者】开启自动搬砖模式")
        self.timer.start(1000)
        self.player.attack()

    def onStop(self):
        self.timer.stop()
        self.player.stand()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F8:
            self.onStart()
        if e.key() == Qt.Key_F12:
            self.onStop()
        if e.key() == Qt.Key_Escape:
            self.close()

    def onInterval(self):

        # 释放技能
        if  self.recogbot.loveyAlive():
            print("【目标检测】还有小可爱活着")
            self.player.cast()

        # 战斗奖励
        if self.recogbot.reward():
            print("【目标检测】战斗奖励")
            self.game.reward()

        # 再次挑战
        if self.recogbot.replay():
            print("【目标检测】再次挑战")
            self.game.replay()

        # 跳过深渊
        if self.recogbot.demon():
            print("【目标检测】跳过深渊")
            self.game.tower()

        # 装备修理
        if self.recogbot.disrepair():
            print("【目标检测】装备修理")
            self.game.repair()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    voyager = Voyager()
    sys.exit(app.exec_())
