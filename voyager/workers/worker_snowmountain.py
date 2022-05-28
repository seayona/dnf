from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from .player_fight_snowmountain import PlayerFightWorker
from .player_fight_attack import PlayerAttackWorker
from .player_fight_cooldown import PlayerSkillCooldownWorker


class GameWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        # 初始化函数，默认
        super(GameWorker, self).__init__()
        self.voyager = voyager
        self.game = voyager.game
        self.recogbot = voyager.recogbot
        self.player = voyager.player

        f = PlayerFightWorker(self.voyager)
        a = PlayerAttackWorker(self.voyager)
        c = PlayerSkillCooldownWorker(self.voyager)

        self.workers = [f, a, c]

    def _run(self):
        # 疲劳值未耗尽，人在城镇中，去搬砖
        if self.recogbot.town() and not self.player.tired():
            print("【一键搬砖】5秒后前往雪山")
            # 防止重复开启线程
            self.game.snow_mountain_start()

        if self.recogbot.lion_clear():
            print("【雪山】狮子头已处理!")
            self.game.lion_clear()

        # 发现雪山入口
        if self.recogbot.entry_snow_mountain():
            print("【雪山】发现雪山入口！")
            self.game.snow_mountain_fight()

        # 战斗奖励
        if self.recogbot.reward():
            print("【雪山】战斗奖励，战斗结束!")
            self.game.reward()

        # 死亡
        if self.recogbot.dead():
            print("【雪山】死亡")
            self.game.revival()

        # 装备修理
        if not self.game.repaired and self.recogbot.bag():
            print("【雪山】装备与分解修理")
            self.game.repair_and_sale()

        # 再次挑战
        if self.recogbot.replay():
            print("【雪山】再次挑战")
            self.game.replay()

        # 疲劳值不足，选择关卡的时候
        if self.recogbot.insufficient_balance() and self.recogbot.close():
            print("【雪山】疲劳值不足")
            self.player.over_fatigued()
            self.game.town()
            self.trigger.emit(str('stop'))

        # 疲劳值不足，人在地下城中，返回城镇
        if self.player.tired() and (self.recogbot.jump() or self.recogbot.result()):
            print("【雪山】疲劳值不足")
            self.game.town()
            self.trigger.emit(str('stop'))

        # 疲劳值不足，打完深渊的时候
        if self.recogbot.insufficient_balance_demon():
            print("【雪山】疲劳值不足，打完深渊的时候")
            self.player.over_fatigued()
            self.game.town()
            self.trigger.emit(str('stop'))

        # 出现确认的弹框？
        if self.recogbot.confirm():
            self.game.confirm()

        if self.recogbot.close():
            self.game.esc()

    def run(self):
        print("【雪山】雪山开始执行")
        for s in self.workers:
            s.start()
        while True:
            self._run()

    def stop(self):
        print("【工作线程】雪山停止执行")
        for s in self.workers:
            s.stop()
        self.terminate()
