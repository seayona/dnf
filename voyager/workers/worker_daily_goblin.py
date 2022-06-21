import time

from PyQt5.QtCore import QThread, pyqtSignal

from .player_fight_snowmountain import PlayerFightWorker
from .player_fight_attack import PlayerAttackWorker
from .player_fight_cooldown import PlayerSkillCooldownWorker
from .worker_daily import DailyWork
from .player_fight_goblin import GoblinFightWorker


class GoblinWorker(DailyWork):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        # 初始化函数，默认
        super(GoblinWorker, self).__init__(voyager, 'goblin', 1)
        self.f = GoblinFightWorker(self.voyager)

    def _recog_entry(self):
        return self.voyager.recogbot.daily_goblin()

    def _recog_work_completed(self):
        return self.voyager.recogbot.daily_goblin_completed()
