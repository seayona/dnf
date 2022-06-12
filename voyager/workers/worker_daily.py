import time

from PyQt5.QtCore import QThread, pyqtSignal

from .player_fight_snowmountain import PlayerFightWorker
from .player_fight_attack import PlayerAttackWorker
from .player_fight_cooldown import PlayerSkillCooldownWorker


class DailyWork(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager, current_work, back_town_wait=5):
        # 初始化函数，默认
        super(DailyWork, self).__init__()
        self.voyager = voyager
        self.running = False
        self.workers = []

        self.current_work = current_work
        self.back_town_wait = back_town_wait

        self.f = PlayerFightWorker(self.voyager)
        self.s = PlayerSkillCooldownWorker(self.voyager)
        self.a = PlayerAttackWorker(self.voyager)

    def init(self):
        self.running = True
        self.workers = [self.f, self.s, self.a]
        for s in self.workers:
            s.start()

    def _recog_entry(self):
        pass

    def _recog_work_completed(self):
        pass

    def _run(self):
        # 人在城镇，去打碳
        if self.voyager.recogbot.town():
            self.voyager.game.daily_start()

        # 发现碳入口
        if self._recog_entry() and not self.voyager.player.daily_status(self.current_work):
            print(f"【{self.current_work}】发现{self.current_work}入口！")
            self.voyager.game.daily_fight(self.current_work)

        # 死亡
        if self.voyager.recogbot.dead():
            self.voyager.game.revival()

        # 人在城镇，去打每日
        if self.voyager.recogbot.town():
            self.voyager.game.daily_start()

        # 战斗已结束，发现再次挑战
        if self.voyager.recogbot.replay():
            self.voyager.game.daily_replay()

        # 死亡
        if self.voyager.recogbot.dead():
            self.voyager.game.revival()

        # 返回日常界面
        if self.voyager.recogbot.daily_town() and not self.voyager.recogbot.replay():
            self.voyager.game.daily_town(self.back_town_wait)

        if self._recog_work_completed():
            print(f"【{self.current_work}】{self.current_work}已刷完！")
            self.voyager.player.over_daily(self.current_work)
            self.voyager.game.back_town_daily()

        if self.voyager.recogbot.daily_confirm_grey() and self.voyager.recogbot.close():
            print(f"【{self.current_work}】{self.current_work}已刷完！不要在点了！")
            self.voyager.player.over_daily(self.current_work)
            self.voyager.game.back_town_daily()

        if self.voyager.recogbot.town() and self.voyager.player.daily_status(self.current_work):
            self.trigger.emit(self.__class__.__name__)

    def run(self):
        self.init()
        print(f"【{self.current_work}】{self.current_work}开始执行")
        while self.running:
            self._run()
            time.sleep(0.5)

    def stop(self):
        print(f"【{self.current_work}】{self.current_work}停止执行")
        for s in self.workers:
            s.stop()
        self.running = False
