import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

from voyager.game import Player, Game
from voyager.infrastructure import Notification
from voyager.recognition import Recogbot
from voyager.workers import GameWorker, PlayerFightWorker, ValleyWorker, AgencyMissionWorker, \
    PlayerMissionFightWorker, PlayerAttackWorker, PlayerSkillCooldownWorker, AutoStriveWorker, AutoLevelUpWorker

print("【探索者】加载UI")
VoyagerWindow, _ = uic.loadUiType("ui/main.ui")


# 【探索者】
class Voyager(QMainWindow, VoyagerWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.timer = QTimer()

        self.notification = Notification()
        self.game = Game()
        self.recogbot = Recogbot()
        self.player = Player('Tyrrell')

        self.workers = []

        print("【探索者】启动成功")
        print("【探索者】按F8键自动搬砖/F12键停止/Esc键退出程序")
        self._init_ui()

    def _init_ui(self):
        self.btn_stop.clicked.connect(self.on_stop_click)
        self.btn_start.clicked.connect(self.on_work_clicked)
        self.btn_valley.clicked.connect(self.on_valley_clicked)
        self.btn_agency.clicked.connect(self.on_agency_mission_clicked)
        self.btn_auto_work.clicked.connect(self.on_auto_work_clicked)
        self.btn_auto_levelup.clicked.connect(self.on_auto_levelup_clicked)

        # UI界面，显示在右上角
        self.move(1560, 0)
        # 置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()

    def _disable(self):
        for btn in [self.btn_start, self.btn_valley, self.btn_agency, self.btn_auto_work]:
            btn.setEnabled(False)

    def _enable(self):
        for btn in [self.btn_start, self.btn_valley, self.btn_agency, self.btn_auto_work]:
            btn.setEnabled(True)

    def _show_message(self, message):
        self.statusBar().showMessage(message)

    def on_auto_work_clicked(self):
        a = AutoStriveWorker()
        a.trigger.connect(self.on_stop_click)
        a.start()
        self.workers.append(a)
        self._disable()

    def on_auto_levelup_clicked(self):
        l = AutoLevelUpWorker()
        l.trigger.connect(self.on_stop_click)
        l.start()
        self.workers.append(l)
        self._disable()

    # 雪山
    def on_work_clicked(self):
        print("【探索者】5秒后前往雪山")

        def callback():
            f = PlayerFightWorker(self.game, self.recogbot, self.player)
            f.trigger.connect(self.on_stop_click)
            f.start()
            self.workers.append(f)

            g = GameWorker(self.game, self.recogbot)
            g.trigger.connect(self.on_stop_click)
            g.start()
            self.workers.append(g)

            s = PlayerSkillCooldownWorker(self.player)
            s.start()
            self.workers.append(s)

            a = PlayerAttackWorker(self.player)
            a.start()
            self.workers.append(a)

            self._disable()

        self.game.snow_mountain_start(callback)

    # 祥瑞溪谷
    def on_valley_clicked(self):
        print("【探索者】5秒后前往祥瑞溪谷")
        self.timer.singleShot(5000, lambda: self.game.valley_start())

        v = ValleyWorker(self.game, self.recogbot)
        v.trigger.connect(self.on_stop_click)
        v.start()
        self.workers.append(v)

        f = PlayerFightWorker(self.game, self.recogbot, self.player)
        f.trigger.connect(self.on_stop_click)
        f.start()
        self.workers.append(f)

        s = PlayerSkillCooldownWorker(self.player)
        s.start()
        self.workers.append(s)

        a = PlayerAttackWorker(self.player)
        a.start()
        self.workers.append(a)

        self._disable()

    # 自动升级
    def on_agency_mission_clicked(self):
        print("【探索者】5秒后开始自动升级")
        self.timer.singleShot(5000, lambda: self.game.agency_mission())

        m = AgencyMissionWorker(self.game, self.recogbot, self.player)
        m.trigger.connect(self.on_agency_mission_stop)
        m.start()
        self.workers.append(m)

        f = PlayerMissionFightWorker(self.game, self.recogbot, self.player)
        f.trigger.connect(self.on_stop_click)
        f.start()
        self.workers.append(f)

        s = PlayerSkillCooldownWorker(self.player)
        s.start()
        self.workers.append(s)

        a = PlayerAttackWorker(self.player)
        a.start()
        self.workers.append(a)

        self._disable()

    def on_stop_click(self):
        print("【探索者】关闭自动搬砖模式")
        for w in self.workers:
            w.stop()
        self.timer.stop()
        self._enable()

    def on_agency_mission_stop(self):
        # Notification().send('升级停止')
        pass

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F8:
            self.on_work_clicked()
        if e.key() == Qt.Key_F12:
            self.on_stop_click()
        if e.key() == Qt.Key_F9:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    voyager = Voyager()
    sys.exit(app.exec_())
