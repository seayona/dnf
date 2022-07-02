import time

from PyQt5.QtCore import QThread, pyqtSignal

from .player_fight_snowmountain import PlayerFightWorker
from .player_fight_attack import PlayerAttackWorker
from .player_fight_cooldown import PlayerSkillCooldownWorker
from .worker_daily import DailyWork


class CarbonWorker(DailyWork):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager, daily_next=False):
        # 初始化函数，默认
        super(CarbonWorker, self).__init__(voyager, 'carbon', 10, daily_next=daily_next)
        self.stage = 4

    def _recog_entry(self):
        return self.voyager.recogbot.daily_carbon()

    def _recog_work_completed(self):
        return self.voyager.recogbot.daily_carbon_completed()
