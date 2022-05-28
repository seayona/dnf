import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

from voyager.game import Player, Game
from voyager.infrastructure import Notification
from voyager.recognition import Recogbot
from voyager.workers import GameWorker, ValleyWorker, AgencyMissionWorker, AutoStriveWorker, AutoLevelUpWorker, \
    DemonWorker, WelfareWorker
from voyager.workers.auto_valley import AutoValleyWorker

print("【探索者】加载UI")
VoyagerWindow, _ = uic.loadUiType("ui/main.ui")


# 【探索者】
class Voyager(QMainWindow, VoyagerWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.game = Game()
        self.recogbot = Recogbot()
        self.player = Player('Tyrrell')
        self.notification = Notification()

        self.workers = []

        print("【探索者】启动成功")
        print("【探索者】按F8键自动搬砖/F12键停止/Esc键退出程序")
        self._init_ui()

    def _init_ui(self):
        self.btn_stop.clicked.connect(self.on_stop_click)

        self.btn_snowmountain.clicked.connect(self.on_work_clicked)
        self.btn_valley.clicked.connect(self.on_valley_clicked)
        self.btn_welfare.clicked.connect(self.on_welfare_clicked)
        self.btn_demon.clicked.connect(self.on_demon_clicked)
        self.btn_agency.clicked.connect(self.on_agency_mission_clicked)

        self.btn_auto_work.clicked.connect(self.on_auto_work_clicked)
        self.btn_auto_valley.clicked.connect(self.on_auto_valley_clicked)
        self.btn_auto_levelup.clicked.connect(self.on_auto_levelup_clicked)

        # UI界面，显示在右上角
        self.move(1560, 0)

        # 置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()
        self.ckbox_auto_valley.setChecked(2)
        self.ckbox_auto_welfare.setChecked(2)

    def _disable(self):
        for btn in [self.btn_snowmountain, self.btn_valley, self.btn_welfare, self.btn_demon, self.btn_agency,
                    self.btn_auto_work, self.btn_auto_valley, self.btn_auto_levelup]:
            btn.setEnabled(False)

    def _enable(self):
        for btn in [self.btn_snowmountain, self.btn_valley, self.btn_welfare, self.btn_demon, self.btn_agency,
                    self.btn_auto_work, self.btn_auto_valley, self.btn_auto_levelup]:
            btn.setEnabled(True)

    def show_message(self, message):
        self.statusBar().showMessage(message)

    # 一键搬砖
    def on_auto_work_clicked(self):
        a = AutoStriveWorker(self)
        a.trigger.connect(self.on_stop_click)
        a.start()

        self.workers = [a]
        self._disable()

    # 一键溪谷
    def on_auto_valley_clicked(self):
        a = AutoValleyWorker(self)
        a.trigger.connect(self.on_stop_click)
        a.start()

        self.workers = [a]
        self._disable()

    # 一键升级
    def on_auto_levelup_clicked(self):
        l = AutoLevelUpWorker(self)
        l.trigger.connect(self.on_stop_click)
        l.start()

        self.workers = [l]
        self._disable()

    # 自动搬砖
    def on_work_clicked(self):
        g = GameWorker(self)
        g.trigger.connect(self.on_stop_click)
        g.start()
        self.workers = [g]
        self._disable()

    # 祥瑞溪谷
    def on_valley_clicked(self):
        g = ValleyWorker(self)
        g.trigger.connect(self.on_stop_click)
        g.start()
        self.workers = [g]
        self._disable()

    # 自动福利
    def on_welfare_clicked(self):
        g = WelfareWorker(self)
        g.trigger.connect(self.on_stop_click)
        g.start()
        self.workers = [g]
        self._disable()

    # 自动深渊
    def on_demon_clicked(self):
        g = DemonWorker(self)
        g.trigger.connect(self.on_stop_click)
        g.start()
        self.workers = [g]
        self._disable()

    # 自动升级
    def on_agency_mission_clicked(self):
        g = AgencyMissionWorker(self)
        g.trigger.connect(self.on_stop_click)
        g.start()
        self.workers = [g]
        self._disable()

    # 停止任务
    def on_stop_click(self):
        print("【探索者】关闭自动搬砖模式")
        for w in self.workers:
            w.stop()

        self._enable()

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
