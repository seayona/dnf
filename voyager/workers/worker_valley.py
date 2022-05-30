import time

from PyQt5.QtCore import QThread, pyqtSignal

from .player_fight_snowmountain import PlayerFightWorker
from .player_fight_attack import PlayerAttackWorker
from .player_fight_cooldown import PlayerSkillCooldownWorker


class ValleyWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        # 初始化函数，默认
        super(ValleyWorker, self).__init__()
        self.voyager = voyager
        self.running = False
        self.workers = []

        self.f = PlayerFightWorker(self.voyager)
        self.s = PlayerSkillCooldownWorker(self.voyager)
        self.a = PlayerAttackWorker(self.voyager)

    def init(self):
        self.running = True
        self.workers = [self.f, self.s, self.a]
        for s in self.workers:
            s.start()

    def _run(self):
        if self.voyager.recogbot.town():
            self.voyager.game.valley_start()

        if self.voyager.recogbot.daliy_valley_completed():
            print(f"【祥瑞溪谷】祥瑞溪谷已刷完！{self.voyager.player}")
            self.voyager.player.over_valley()
            self.voyager.game.esc()
            self.voyager.game.esc()
            return

        if self.voyager.recogbot.town() and not self.voyager.player.valley:
            self.trigger.emit(str('stop'))
            return

        if not self.voyager.player.valley and not self.voyager.recogbot.town():
            self.voyager.game.esc()
            return

            # 发现祥瑞溪谷入口
        if self.voyager.recogbot.daily_valley():
            print("【祥瑞溪谷】发现祥瑞溪谷入口！")
            self.voyager.game.valley_fight()

        # 溪谷再次挑战
        if self.voyager.recogbot.replay():
            self.voyager.game.valley_replay()

        # 死亡
        if self.voyager.recogbot.dead():
            self.voyager.game.revival()

        # 返回日常界面
        if self.voyager.recogbot.daily_valley_town():
            self.voyager.game.valley_town()

    def run(self):
        self.init()
        print("【祥瑞溪谷】祥瑞溪谷开始执行")
        while self.running:
            self._run()
            time.sleep(0.5)

    def stop(self):
        print("【祥瑞溪谷】祥瑞溪谷停止执行")
        for s in self.workers:
            s.stop()
        self.running = False
