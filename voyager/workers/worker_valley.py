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

        # 人在城镇，去打溪谷
        if self.voyager.recogbot.town():
            self.voyager.game.valley_start()

        # 发现祥瑞溪谷入口
        if self.voyager.recogbot.daily_valley() and not self.voyager.player.shine():
            print("【祥瑞溪谷】发现祥瑞溪谷入口！")
            self.voyager.game.valley_fight()

        # 战斗已结束，溪谷再次挑战
        if self.voyager.recogbot.replay():
            self.voyager.game.valley_replay()

        # 死亡
        if self.voyager.recogbot.dead():
            self.voyager.game.revival()

        # 返回日常界面
        if self.voyager.recogbot.daily_valley_town() and not self.voyager.recogbot.replay():
            self.voyager.game.valley_town()

        if self.voyager.recogbot.daliy_valley_completed():
            print(f"【祥瑞溪谷】祥瑞溪谷已刷完！")
            self.voyager.player.over_valley()
            self.voyager.game.back_town_valley()

        if self.voyager.recogbot.valley_confirm_grey() and self.voyager.recogbot.close():
            print(f"【祥瑞溪谷】祥瑞溪谷已刷完！不要在点了！")
            self.voyager.player.over_valley()
            self.voyager.game.back_town_valley()

        if self.voyager.recogbot.town() and self.voyager.player.shine():
            self.trigger.emit(str('stop'))

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
