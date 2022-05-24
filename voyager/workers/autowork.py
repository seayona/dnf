from configparser import ConfigParser

from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QEventLoop

from voyager.game import Game, Player
from voyager.infrastructure import Notification
from voyager.recognition import Recogbot
from voyager.workers import PlayerFightWorker, GameWorker, PlayerSkillCooldownWorker, PlayerAttackWorker
from voyager.workers.auto import Auto

class AutoStriveWorker(Auto):

    def __init__(self):
        # 初始化函数，默认
        super(AutoLevelUp, self).__init__('Strive')

    def _init_worker(self):
        # 战斗线程
        f = PlayerFightWorker(self.game, self.recogbot, self.player)
        f.trigger.connect(self._working_stop)
        self.workers.append(f)

        # 雪山场景检测
        g = GameWorker(self.game, self.recogbot)
        g.trigger.connect(self._working_stop)
        self.workers.append(g)

        a = PlayerAttackWorker(self.player)
        a.trigger.connect(self._working_stop)
        self.workers.append(a)

        c = PlayerSkillCooldownWorker(self.player)
        c.trigger.connect(self._working_stop)
        self.workers.append(c)



    def _run(self):
        # 如果角色疲劳值耗尽，并且在城镇中，切换角色
        if self.player.tired() and self.recogbot.town():
            # self.trigger.emit('stop')
            # 切换成功，设置当前角色
            self._switch_player()

        # 疲劳值未耗尽，人在城镇中，去搬砖
        if self.recogbot.town() and not self.player.tired():
            print(f"【自动搬砖】疲劳值还有，人在城镇中，去搬砖")
            print("【自动搬砖】5秒后前往雪山")
            # 防止重复开启线程
            self.game.snow_mountain_start(self._fight)

        # 疲劳值未耗尽，人在地下城中，继续战斗
        if not self.working and (self.recogbot.result() or self.recogbot.jump()) and not self.player.tired():
            print(f"【自动搬砖】疲劳值还有，人在地下城中，继续战斗")
            # 防止重复开启线程
            self._fight()

        # 疲劳值不足，人在地下城中，返回城镇
        if self.player.tired() and (self.recogbot.jump() or self.recogbot.result()):
            print(f"【自动搬砖】疲劳值不足，返回城镇")
            self._working_stop()
            self.game.town()

        if self.recogbot.confirm():
            self.game.confirm()

        # 疲劳值不足，打完深渊图的时候，返回城镇
        if self.recogbot.insufficient_balance_demon():
            print(f"【自动搬砖】疲劳值不足，返回城镇")
            self._working_stop()
            self.player.over_fatigued()

        # 疲劳值不足，再次挑战的时候，返回城镇
        if self.recogbot.insufficient_balance():
            print(f"【自动搬砖】疲劳值不足，返回城镇")
            self._working_stop()
            self.player.over_fatigued()

