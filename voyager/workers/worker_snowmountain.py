import datetime
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
        self.last_out_stuck = None

    def init(self):
        self.last_out_stuck = datetime.datetime.now()
        self.running = True
        self.workers = [self.f, self.a, self.c]
        for s in self.workers:
            s.start()

    def _run(self):
        cls = self.voyager.recogbot.detect()

        # 武器报废
        if cls['door'][0] and self.voyager.recogbot.disrepair():
            self.voyager.player.stand()
            self.voyager.game.repair()

        if self.voyager.recogbot.overweight() and not self.voyager.player.repair:
            self.voyager.game.repair_and_sale(cls['bag'], callback=lambda: self.voyager.player.repaired())

        # 疲劳值未耗尽，人在城镇中，去搬砖
        if not self.voyager.player.tired() and self.voyager.recogbot.town():
            print("【一键搬砖】5秒后前往雪山")
            self.voyager.game.snow_mountain_start()

        # 疲劳值不足，人在地下城，战斗已结束
        if self.voyager.player.tired() and cls['result'][0]:
            print("【雪山】疲劳值不足")
            self.voyager.game.back_town_dungeon(reset=lambda: self.voyager.player.new_game())

        #  已进入狮子头房间
        if self.voyager.recogbot.lion_clear():
            print("【雪山】狮子头已处理!")
            self.voyager.player.lion_clear()

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
            self.voyager.game.back_town_mission(reset=lambda: self.voyager.player.new_game())

        # 深渊已刷完&开门
        if cls['passing'][0] and cls['door'][0]:
            print("【雪山】疲劳值不足")
            self.voyager.game.back_town(cls['setting'], reset=lambda: self.voyager.player.new_game())

        if self.voyager.recogbot.home():
            self.voyager.game.back_home(reset=lambda: self.voyager.player.new_game())

        if self.voyager.player.repair and self.voyager.recogbot.back():
            self.voyager.player.new_game()
            self.voyager.game.back()

        if self.voyager.recogbot.back_share():
            self.voyager.game.back_share()

        if self.voyager.player.tired() and self.voyager.recogbot.town() and not self.voyager.player.repair:
            self.voyager.game.repair_and_sale(cls['bag'], callback=lambda: self.voyager.player.repaired())

        # 疲劳值耗尽，人在城镇
        if self.voyager.player.tired() and self.voyager.recogbot.town() and self.voyager.player.repair:
            self.trigger.emit(self.__class__.__name__)

        # 战斗已结束，再次挑战
        if cls['result'][
            0] and self.voyager.player.repair and not self.voyager.player.tired():
            print("【雪山】再次挑战")
            self.voyager.game.replay(reset=lambda: self.voyager.player.new_game())
            self.count += 1

        # 出现对话时按Esc跳过
        if self.voyager.recogbot.talk_skip():
            self.voyager.game.esc()

        # 再次挑战弹窗
        if self.voyager.recogbot.replay_prop():
            self.voyager.game.confirm()

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
