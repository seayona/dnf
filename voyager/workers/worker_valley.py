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
        self.game = voyager.game
        self.recogbot = voyager.recogbot
        self.player = voyager.player

        f = PlayerFightWorker(self.voyager)
        s = PlayerSkillCooldownWorker(self.voyager)
        a = PlayerAttackWorker(self.voyager)

        self.workers = [f, s, a]

    def _run(self):

        if self.recogbot.town():
            self.game.valley_start()

        if self.recogbot.daliy_valley_completed():
            print(f"【祥瑞溪谷】祥瑞溪谷已刷完！{self.player}")
            self.player.over_valley()
            self.game.esc()
            self.trigger.emit(str('stop'))
            return

        # 发现祥瑞溪谷入口
        if self.recogbot.daily_valley():
            print("【祥瑞溪谷】发现祥瑞溪谷入口！")
            self.game.valley_fight()

        # 溪谷再次挑战
        if self.recogbot.replay():
            self.game.valley_replay()

        # 死亡
        if self.recogbot.dead():
            self.game.revival()

        # 返回日常界面
        if self.recogbot.daily_valley_town():
            self.game.valley_town()

    def run(self):
        print("【祥瑞溪谷】祥瑞溪谷开始执行")
        for s in self.workers:
            s.start()
        while True:
            self._run()

    def stop(self):
        print("【祥瑞溪谷】祥瑞溪谷停止执行")
        for s in self.workers:
            s.stop()
        self.terminate()
