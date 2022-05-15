import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt, QBasicTimer, QTimer
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QDesktopWidget

from game import Player, Game
from recognition import Recogbot
from voyager.control import press

VoyagerWindow, _ = uic.loadUiType("ui/main.ui")


# 【探索者】
class Voyager(QMainWindow, VoyagerWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.timer = QTimer()

        self.game = Game()
        self.recogbot = Recogbot()
        self.player = Player()

        print("【探索者】启动成功")
        print("【探索者】按F8键自动搬砖/F12键停止/Esc键退出程序")


        # UI界面，显示在右上角
        self.move(1560,0)

        self.btn_stop.clicked.connect(self.onstop)
        self.btn_start.clicked.connect(self.on_snow_mountain_clicked)
        self.btn_valley.clicked.connect(self.on_valley_clicked)
        self.btn_agency.clicked.connect(self.on_agency_mission_clicked)

        # 置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.show()


    # 雪山
    def on_snow_mountain_clicked(self):
        print("【探索者】5秒后前往雪山")
        self.timer.stop()
        self.timer.start(1000)
        self.timer.timeout.connect(self._auto_snow_mountain)
        self.timer.singleShot(5000, lambda:self.game.snow_mountain_start())
        self.player.attack()
    # 祥瑞溪谷
    def on_valley_clicked(self):
        print("【探索者】5秒后前往祥瑞溪谷")
        self.timer.start(1000)
        self.timer.timeout.connect(self._auto_valley)
        self.timer.singleShot(5000, lambda:self.game.valley_start())
        self.player.attack()

    # 自动升级
    def on_agency_mission_clicked(self):
        print("【探索者】5秒后开始自动升级")
        self.timer.start(1000)
        self.timer.timeout.connect(self._auto_agency_mission)
        self.timer.singleShot(5000, lambda:self.game.agency_mission())
        self.player.attack()

    def onstop(self):
        print("【探索者】关闭自动搬砖模式")
        self.timer.stop()
        self.player.stand()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F8:
            self.onstart()
        if e.key() == Qt.Key_F12:
            self.onstop()
        if e.key() == Qt.Key_Escape:
            self.close()

    def _auto_valley(self):
        if self.recogbot.daliy_valley_completed():
            print("【目标检测】祥瑞溪谷已刷完！")
            self.onstop()
            return

        # 发现祥瑞溪谷入口
        if self.recogbot.daily_valley():
            print("【目标检测】发现祥瑞溪谷入口！")
            self.game.valley_fight()

        # 释放觉醒
        if self.recogbot.boss_valley():
            print("【目标检测】发现祥瑞溪谷Boss!")
            self.player.finisher()
            self.player.cast()

        # 死亡
        if self.recogbot.dead():
            self.game.revival()

        # 战斗结束
        if self.recogbot.bag():
            self.game.repair()

        # 返回日常界面
        if self.recogbot.daily_valley_town():
            self.game.valley_town()

    def _auto_snow_mountain(self):
        # 发现雪山入口
        if self.recogbot.entry_snow_mountain():
            print("【目标检测】发现雪山入口！")
            self.game.snow_mountain_fight()

        # 释放技能
        if self.recogbot.loveyAlive():
            print("【目标检测】还有小可爱活着")
            self.player.cast()

        # 释放觉醒
        if self.recogbot.boss():
            print("【目标检测】发现Boss!")
            self.player.finisher()

        if self.recogbot.lion_clear():
            print("【目标检测】狮子头已处理!")
            self.game.lion_clear()

        # 狮子头
        if self.recogbot.lion():
            print("【目标检测】发现狮子头!")
            self.game.lion_clear()
            self.player.finisher()
            self.player.cast()

        # 发现狮子头入口
        if self.game.lionAlive and self.recogbot.door() and self.recogbot.lion_entry():
            print("【目标检测】发现狮子头入口!")
            self.player.stand()
            self.player.right()

        # 战斗奖励
        if self.recogbot.reward():
            print("【目标检测】战斗奖励，战斗结束!")
            self.game.reward()

        # 死亡
        if self.recogbot.dead():
            self.game.revival()

        # 装备修理
        if not self.game.repaired and self.recogbot.bag():
            self.game.repair()

        # 装备分解
        if not self.game.saled and self.recogbot.bag():
            self.game.sale()

        # 再次挑战
        if self.recogbot.replay():
            self.game.replay()

        # 疲劳值不足
        if self.recogbot.insufficient_balance():
            self.game.snow_mountain_finish()
            self.onstop()

    def _auto_agency_mission(self):

        if self.recogbot.talk():
            self.game.talk_skip()

        if self.recogbot.next():
            self.game.next()

        if self.recogbot.next_agency():
            self.game.next_agency()

        if self.recogbot.next_agency_confirm():
            self.game.next_agency_confirm()

        if self.recogbot.confirm():
            self.game.confirm()

        # 返回
        if self.recogbot.back():
            self.game.back()

        # 自动装备
        if self.recogbot.equip():
            self.game.equip()

        # 点击关闭
        if self.recogbot.click_close():
            self.game.click_close()

        if self.recogbot.setting() and not self.recogbot.door():
            print("【目标检测】门没开，无脑输出")
            self.player.cast_random()

        # 装备修理
        if not self.game.repaired and self.recogbot.bag():
            self.game.repair()

        # 装备分解
        if not self.game.saled and self.recogbot.bag():
            self.game.sale()

        # 死亡
        if self.recogbot.dead():
            self.game.revival()

        # 疲劳值不足
        if self.recogbot.insufficient_balance():
            self.game.agency_mission_finish()
            self.onstop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    voyager = Voyager()
    sys.exit(app.exec_())
