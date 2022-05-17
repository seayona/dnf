import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

from voyager.game import Player, Game
from voyager.recognition import Recogbot
from voyager.workers import GameWorker, PlayerFightWorker, ValleyWorker, AgencyMissionWorker, \
    PlayerMissionFightWorker, PlayerAttackTimer, PlayerSkillCooldownTimer

VoyagerWindow, _ = uic.loadUiType("ui/main.ui")


# 【探索者】
class Voyager(QMainWindow, VoyagerWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.timer = QTimer()

        self.workers = []
        self.game = Game()
        self.recogbot = Recogbot()
        self.player = Player('asura')

        print("【探索者】启动成功")
        print("【探索者】按F8键自动搬砖/F12键停止/Esc键退出程序")

        # UI界面，显示在右上角
        self.move(1560, 0)

        self.btn_stop.clicked.connect(self.onstop)
        self.btn_start.clicked.connect(self.on_snow_mountain_clicked)
        self.btn_valley.clicked.connect(self.on_valley_clicked)
        self.btn_agency.clicked.connect(self.on_agency_mission_clicked)

        # 置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()

    def _disable(self):
        self.btn_start.setEnabled(False)
        self.btn_valley.setEnabled(False)
        self.btn_agency.setEnabled(False)

    def _enable(self):
        self.btn_start.setEnabled(True)
        self.btn_valley.setEnabled(True)
        self.btn_agency.setEnabled(True)

    # 雪山
    def on_snow_mountain_clicked(self):
        print("【探索者】5秒后前往雪山")
        self.timer.singleShot(5000, lambda: self.game.snow_mountain_start())

        f = PlayerFightWorker(self.game, self.recogbot, self.player)
        f.trigger.connect(self.onstop)
        f.start()
        self.workers.append(f)

        g = GameWorker(self.game, self.recogbot)
        g.trigger.connect(self.onstop)
        g.start()
        self.workers.append(g)

        s = PlayerSkillCooldownTimer(self.player)
        s.start()
        self.workers.append(s)

        a = PlayerAttackTimer(self.player)
        a.start()
        self.workers.append(a)

        self._disable()

    # 祥瑞溪谷
    def on_valley_clicked(self):
        print("【探索者】5秒后前往祥瑞溪谷")
        self.timer.singleShot(5000, lambda: self.game.valley_start())

        v = ValleyWorker(self.game, self.recogbot)
        v.trigger.connect(self.onstop)
        v.start()
        self.workers.append(v)

        f = PlayerFightWorker(self.game, self.recogbot, self.player)
        f.trigger.connect(self.onstop)
        f.start()
        self.workers.append(f)

        s = PlayerSkillCooldownTimer(self.player)
        s.start()
        self.workers.append(s)

        a = PlayerAttackTimer(self.player)
        a.start()
        self.workers.append(a)

        self._disable()

    # 自动升级
    def on_agency_mission_clicked(self):
        print("【探索者】5秒后开始自动升级")
        self.timer.singleShot(5000, lambda: self.game.agency_mission())

        m = AgencyMissionWorker(self.game, self.recogbot, self.player)
        m.trigger.connect(self.onstop)
        m.start()
        self.workers.append(m)

        f = PlayerMissionFightWorker(self.game, self.recogbot, self.player)
        f.trigger.connect(self.onstop)
        f.start()
        self.workers.append(f)

        s = PlayerSkillCooldownTimer(self.player)
        s.start()
        self.workers.append(s)

        a = PlayerAttackTimer(self.player)
        a.start()
        self.workers.append(a)

        self._disable()

    def onstop(self):
        print("【探索者】关闭自动搬砖模式")
        for w in self.workers:
            w.stop()
        self.timer.stop()
        self._enable()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F8:
            self.onstart()
        if e.key() == Qt.Key_F12:
            self.onstop()
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    voyager = Voyager()
    sys.exit(app.exec_())
