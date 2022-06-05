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
        self.count = 0

    def init(self):
        self.running = True
        self.workers = [self.f, self.a, self.c]
        for s in self.workers:
            s.start()

    def _run(self):
        cls = self.voyager.recogbot.detect()

        # 第一次一定修理
        if self.count % 4 == 0 and not self.voyager.recogbot.disrepair():
            self.voyager.game.repaired = True

        # 武器报废
        if cls['door'][0] and self.voyager.recogbot.disrepair():
            self.voyager.player.stand()
            self.voyager.game.repair()

        # 疲劳值未耗尽，人在城镇中，去搬砖
        if not self.voyager.player.tired() and self.voyager.recogbot.town():
            print("【一键搬砖】5秒后前往雪山")
            self.voyager.game.snow_mountain_start()

        # 疲劳值不足，人在地下城，战斗已结束
        if self.voyager.player.tired() and cls['result'][0]:
            print("【雪山】疲劳值不足")
            self.voyager.game.back_town_dungeon()

        #  已进入狮子头房间
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

        # 疲劳值不足，再次挑战的时候
        if self.voyager.recogbot.insufficient_balance():
            print("【雪山】疲劳值不足")
            self.voyager.player.over_fatigued()
            self.voyager.game.confirm()

        # 疲劳值不足，选择关卡的时候
        if self.voyager.recogbot.insufficient_balance_entry():
            print("【雪山】疲劳值不足")
            self.voyager.player.over_fatigued()
            self.voyager.game.back_town_mission()

        # 疲劳值不足，深渊的时候
        if cls['passing'][0] and cls['door'][0]:
            print("【雪山】疲劳值不足")
            self.voyager.game.back_town(cls['setting'])

        # 疲劳值耗尽，人在城镇
        if self.voyager.player.tired() and self.voyager.recogbot.town():
            self.trigger.emit(self.__class__.__name__)

        # 战斗已结束，还没有修理
        if not self.voyager.game.repaired and cls['result'][0] and cls['bag'][0] and cls['bag'][2] < 200:
            print("【雪山】装备与分解修理", cls['bag'])
            self.voyager.game.repair_and_sale(cls['bag'])

        # 战斗已结束，再次挑战
        if cls['result'][0] and self.voyager.recogbot.replay() and self.voyager.game.repaired:
            print("【雪山】再次挑战")
            self.voyager.game.replay()
            self.count += 1

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
