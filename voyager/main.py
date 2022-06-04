import sys
from configparser import ConfigParser

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox

from voyager.game import Player, Game
from voyager.infrastructure import Notification
from voyager.infrastructure.matric import Matric
from voyager.recognition import Recogbot
from voyager.workers import GameWorker, ValleyWorker, AgencyMissionWorker, AutoStriveWorker, AutoLevelUpWorker, \
    DemonWorker, WelfareWorker, AutoWelfareWorker
from voyager.workers.auto_valley import AutoValleyWorker
from voyager.workers.matric import MatricWorker

print("【探索者】加载UI")
VoyagerWindow, _ = uic.loadUiType("ui/main.ui")


# 【探索者】
class Voyager(QMainWindow, VoyagerWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)

        print("【探索者】读取角色配置")
        config = ConfigParser()
        config.read('conf/player.ini', encoding='UTF-8')
        players = config.sections()
        print("【探索者】读取到的角色", players)
        self.players = list(players)
        self.strivers = list(filter(lambda p: config.get(p, 'Work') == 'Strive', players))
        self.levelup = list(filter(lambda p: config.get(p, 'Work') == 'LevelUp', players))

        self.game = Game()
        self.recogbot = Recogbot()
        self.player = Player(players[0])
        self.notification = Notification()
        self.matric = Matric()

        self.workers = []

        print("【探索者】启动成功")
        print("【探索者】按F8键自动搬砖/F12键停止/Esc键退出程序")
        self._init_ui()

        self.matric_worker = MatricWorker(self)

    def _switch_player(self, q):
        self.player = Player(q.text())
        conf = ConfigParser()
        conf.read('./conf/auto.ini')
        conf.set('Strive', 'Player', q.text())
        conf.set('LevelUp', 'Player', q.text())
        conf.set('Valley', 'Player', q.text())
        conf.set('Welfare', 'Player', q.text())
        conf.write(open('./conf/auto.ini', "w"))
        self.show_message(f"角色【{q.text()}】配置已加载")

    def _init_ui(self):

        # UI界面，显示在右上角
        self.move(1560, 0)

        # 初始化角色列表
        m = self.menuBar().actions()[0].menu()
        m.triggered.connect(self._switch_player)

        for s in self.strivers:
            m.addAction(s)

        m.addSeparator()
        for s in self.levelup:
            m.addAction(s)

        # 置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()

    def _disable(self):
        for btn in [self.btn_snowmountain, self.btn_valley, self.btn_welfare, self.btn_demon, self.btn_agency,
                    self.btn_auto_work, self.btn_auto_valley, self.btn_auto_levelup, self.btn_auto_welfare]:
            btn.setEnabled(False)

    def _enable(self):
        for btn in [self.btn_snowmountain, self.btn_valley, self.btn_welfare, self.btn_demon, self.btn_agency,
                    self.btn_auto_work, self.btn_auto_valley, self.btn_auto_levelup, self.btn_auto_welfare]:
            btn.setEnabled(True)

    def show_message(self, message):
        self.statusBar().showMessage(message)

    # 一键搬砖
    @pyqtSlot()
    def on_btn_auto_work_clicked(self):
        a = AutoStriveWorker(self)
        a.trigger.connect(self.on_btn_stop_clicked)
        a.start()

        self.workers = [a]
        self._disable()

    # 一键溪谷
    @pyqtSlot()
    def on_btn_auto_valley_clicked(self):
        a = AutoValleyWorker(self)
        a.trigger.connect(self.on_btn_stop_clicked)
        a.start()

        self.workers = [a]
        self._disable()

    # 一键升级
    @pyqtSlot()
    def on_widget_switch_clicked(self):
        if self.widget_switch.state:
            self.matric_worker.start()
        else:
            self.matric_worker.stop()

    # 一键升级
    @pyqtSlot()
    def on_btn_auto_levelup_clicked(self):
        l = AutoLevelUpWorker(self)
        l.trigger.connect(self.on_btn_stop_clicked)
        l.start()

        self.workers = [l]
        self._disable()

    # 一键福利
    @pyqtSlot()
    def on_btn_auto_welfare_clicked(self):
        l = AutoWelfareWorker(self)
        l.trigger.connect(self.on_btn_stop_clicked)
        l.start()

        self.workers = [l]
        self._disable()

    # 自动搬砖
    @pyqtSlot()
    def on_btn_snowmountain_clicked(self):
        g = GameWorker(self)
        g.trigger.connect(self.on_btn_stop_clicked)
        g.start()
        self.workers = [g]
        self._disable()

    # 祥瑞溪谷
    @pyqtSlot()
    def on_btn_valley_clicked(self):
        g = ValleyWorker(self)
        g.trigger.connect(self.on_btn_stop_clicked)
        g.start()
        self.workers = [g]
        self._disable()

    # 自动福利
    @pyqtSlot()
    def on_btn_welfare_clicked(self):
        g = WelfareWorker(self)
        g.trigger.connect(self.on_btn_stop_clicked)
        g.start()
        self.workers = [g]
        self._disable()

    # 自动深渊
    @pyqtSlot()
    def on_btn_demon_clicked(self):
        g = DemonWorker(self)
        g.trigger.connect(self.on_btn_stop_clicked)
        g.start()
        self.workers = [g]
        self._disable()

    # 自动升级
    @pyqtSlot()
    def on_btn_agency_clicked(self):
        g = AgencyMissionWorker(self)
        g.trigger.connect(self.on_btn_stop_clicked)
        g.start()
        self.workers = [g]
        self._disable()

    # 停止任务
    @pyqtSlot()
    def on_btn_stop_clicked(self):
        print("【探索者】关闭自动模式")
        for w in self.workers:
            w.stop()
        self.game = Game()
        self.matric = Matric()
        self._enable()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F8:
            self.on_work_clicked()
        if e.key() == Qt.Key_F12:
            self.on_btn_stop_clicked()
        if e.key() == Qt.Key_F9:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    voyager = Voyager()
    sys.exit(app.exec_())
