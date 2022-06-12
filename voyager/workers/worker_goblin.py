import time

from PyQt5.QtCore import QThread, pyqtSignal

from .player_fight_snowmountain import PlayerFightWorker
from .player_fight_attack import PlayerAttackWorker
from .player_fight_cooldown import PlayerSkillCooldownWorker


class GoblinWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        # 初始化函数，默认
        super(GoblinWorker, self).__init__()
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
        # 人在城镇，去打哥布林
        if self.voyager.recogbot.town():
            self.voyager.game.daily_start()

        # 发现哥布林入口
        if self.voyager.recogbot.daily_goblin() and not self.voyager.player.rich():
            print("【哥布林】发现哥布林入口！")
            self.voyager.game.daily_fight('goblin')

        # 死亡
        if self.voyager.recogbot.dead():
            self.voyager.game.revival()

        if self.voyager.recogbot.daily_result():
            self.voyager.game.esc()

        # 返回日常界面
        if self.voyager.recogbot.daily_town():
            self.voyager.game.daily_town(1)

        if self.voyager.recogbot.daily_goblin_completed():
            print(f"【哥布林】哥布林已刷完！")
            self.voyager.player.over_goblin()
            self.voyager.game.back_town_daily()

        if self.voyager.recogbot.daily_confirm_grey() and self.voyager.recogbot.close():
            print(f"【哥布林】哥布林已刷完！不要在点了！")
            self.voyager.player.over_goblin()
            self.voyager.game.back_town_daily()

        if self.voyager.recogbot.town() and self.voyager.player.rich():
            self.trigger.emit(self.__class__.__name__)

    def run(self):
        self.init()
        print("【哥布林】哥布林开始执行")
        while self.running:
            self._run()
            time.sleep(0.5)

    def stop(self):
        print("【哥布林】哥布林停止执行")
        for s in self.workers:
            s.stop()
        self.running = False
