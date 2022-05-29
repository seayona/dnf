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
        self.running = False
        self.workers = []

        self.f = PlayerFightWorker(self.voyager)
        self.a = PlayerAttackWorker(self.voyager)
        self.c = PlayerSkillCooldownWorker(self.voyager)

    def init(self):
        self.running = True
        self.workers = [self.f, self.a, self.c]
        for s in self.workers:
            s.start()

    def _run(self):

        if self.voyager.player.tired() and (self.voyager.recogbot.jump() or self.voyager.recogbot.result()):
            print("【雪山】疲劳值不足")
            self.voyager.game.town()

        # 疲劳值未耗尽，人在城镇中，去搬砖
        if self.voyager.recogbot.town() and not self.voyager.player.tired():
            print("【一键搬砖】5秒后前往雪山")
            # 防止重复开启线程
            self.voyager.game.snow_mountain_start()

        if self.voyager.recogbot.lion_clear():
            print("【雪山】狮子头已处理!")
            self.voyager.game.lion_clear()

        # 发现雪山入口
        if self.voyager.recogbot.entry_snow_mountain():
            print("【雪山】发现雪山入口！")
            self.voyager.game.snow_mountain_fight()

        # 战斗奖励
        if self.voyager.recogbot.reward():
            print("【雪山】战斗奖励，战斗结束!")
            self.voyager.game.reward()

        # 死亡
        if self.voyager.recogbot.dead():
            print("【雪山】死亡")
            self.voyager.game.revival()

        # 装备修理
        if not self.voyager.game.repaired and self.voyager.recogbot.bag():
            print("【雪山】装备与分解修理")
            self.voyager.game.repair_and_sale()

        # 再次挑战
        if self.voyager.recogbot.replay():
            print("【雪山】再次挑战")
            self.voyager.game.replay()

        # 疲劳值不足，选择关卡的时候
        if self.voyager.recogbot.insufficient_balance():
            print("【雪山】疲劳值不足")
            self.voyager.player.over_fatigued()
            self.voyager.game.town()

        # 疲劳值不足，打完深渊的时候
        if self.voyager.recogbot.insufficient_balance_demon():
            print("【雪山】疲劳值不足，打完深渊的时候")
            self.voyager.player.over_fatigued()
            self.voyager.game.town()

        if self.voyager.recogbot.town() and self.voyager.player.tired():
            self.trigger.emit(str('stop'))

        # 出现确认的弹框？
        if self.voyager.recogbot.confirm():
            self.voyager.game.confirm()

        if self.voyager.recogbot.close():
            self.voyager.game.esc()

    def run(self):
        self.init()
        print("【雪山】雪山开始执行")
        while self.running:
            self._run()

    def stop(self):
        print("【工作线程】雪山停止执行")
        for s in self.workers:
            s.stop()
        self.running = False
