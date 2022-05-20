import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow

from configparser import ConfigParser

from voyager.game import Player, Game
from voyager.infrastructure import Notification
from voyager.recognition import Recogbot
from voyager.workers import GameWorker, PlayerFightWorker, ValleyWorker, AgencyMissionWorker, \
    PlayerMissionFightWorker, PlayerAttackTimer, PlayerSkillCooldownTimer

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
        # self.player = Player('blademaster')

        self.workers = []

        print("【探索者】启动成功")
        print("【探索者】按F8键自动搬砖/F12键停止/Esc键退出程序")
        self._init_ui()
        self._init_work()

    def _init_ui(self):
        self.btn_stop.clicked.connect(self.onstop)
        self.btn_start.clicked.connect(self.on_work_clicked)
        self.btn_valley.clicked.connect(self.on_valley_clicked)
        self.btn_agency.clicked.connect(self.on_agency_mission_clicked)
        self.btn_auto_work.clicked.connect(self.on_auto_work)

        # UI界面，显示在右上角
        self.move(1560, 0)
        # 置顶
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.show()

    def _init_work(self):
        print("【探索者】读取角色配置")
        config = ConfigParser()
        config.read('conf/player.ini', encoding='UTF-8')
        self.players = config.sections()
        print("【探索者】读取到的角色", self.players)
        self.strivers = list(filter(lambda p: config.get(p, 'Work') == 'Strive', self.players))
        print("【探索者】读取到的砖工", self.strivers)
        self.boys = list(filter(lambda p: config.get(p, 'Work') == 'LevelUp', self.players))
        print("【探索者】读取到的小号", self.boys)

    def _disable(self):
        for btn in [self.btn_start, self.btn_valley, self.btn_agency, self.btn_auto_work]:
            btn.setEnabled(False)

    def _enable(self):
        for btn in [self.btn_start, self.btn_valley, self.btn_agency, self.btn_auto_work]:
            btn.setEnabled(True)

    def _current(self):
        conf = ConfigParser()
        conf.read('./conf/auto.ini')
        player = conf.get('Strive', 'Player')
        return player

    def _current_striver_update(self, value):
        conf = ConfigParser()
        conf.read('./conf/auto.ini')
        conf.set('Strive', 'Player', value)

    def _next_striver(self):
        current = self._current()
        if current in self.strivers:
            i = self.strivers.index(current)
            if i + 1 == len(self.strivers):
                print("【探索者】所有角色搬砖已完成")
                self.notification.send("所有角色搬砖已完成")
            next_striver = self.strivers[i + 1]
        else:
            next_striver = self.strivers[0]
        # 更新配置
        self._current_striver_update(next_striver)
        return next_striver

    def _switch_striver(self):
        striver = self._current()
        if striver is None or striver not in self.strivers:
            striver = self.strivers[0]
        # 更新配置
        self._current_striver_update(striver)
        # 初始化角色
        self.player = Player(striver)
        return striver

    # 角色搬砖完成
    def on_striver_completed(self):
        # 停止脚本
        self.onstop()
        # 通知
        current = self._current()
        self.notification.send(f'【{current}】疲劳值耗尽')
        # 切换到下一个角色
        next_striver = self._next_striver()
        # 选择角色
        self._switch_striver()
        # 通知
        self.notification.send(f'【{next_striver}】开始搬砖')
        # 开始搬砖
        self.on_work_clicked()

    def on_auto_work(self):
        striver = self._switch_striver()
        print("【探索者】5秒后开始自动搬砖")
        # 切换到此角色
        self.statusBar().showMessage(f"【{striver}】开始切换角色...")

        def callback(striver):
            self.statusBar().showMessage(f"【{striver}】角色切换完成，5s后出发前往雪山")
            print("【探索者】角色切换完成，5s后出发前往雪山")
            self.on_work_clicked()

        self.timer.singleShot(5000, lambda: self.game.switch(striver, callback))
        self._disable()

    # 雪山
    def on_work_clicked(self):
        print("【探索者】5秒后前往雪山")
        def callback():
            f = PlayerFightWorker(self.game, self.recogbot, self.player)
            f.trigger.connect(self.onstop)
            f.start()
            self.workers.append(f)

            g = GameWorker(self.game, self.recogbot)
            g.trigger.connect(self.on_striver_completed)
            g.start()
            self.workers.append(g)

            s = PlayerSkillCooldownTimer(self.player)
            s.start()
            self.workers.append(s)

            a = PlayerAttackTimer(self.player)
            a.start()
            self.workers.append(a)

            self._disable()

        self.timer.singleShot(10000, lambda: self.game.snow_mountain_start(callback))

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

        # print('【选择角色】5秒后选择角色Livana')
        # self.timer.singleShot(5000, lambda: self.game.switch('Livana'))

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_F8:
            self.onstart()
        if e.key() == Qt.Key_F12:
            self.onstop()
        if e.key() == Qt.Key_F9:
            self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    voyager = Voyager()
    sys.exit(app.exec_())
