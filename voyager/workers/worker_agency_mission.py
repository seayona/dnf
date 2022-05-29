from PyQt5.QtCore import QThread, pyqtSignal

from .player_fight_agency_mission import PlayerMissionFightWorker
from .player_fight_attack import PlayerAttackWorker
from .player_fight_cooldown import PlayerSkillCooldownWorker


class AgencyMissionWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        # 初始化函数，默认
        super(AgencyMissionWorker, self).__init__()
        self.voyager = voyager
        self.running = False

        self.f = PlayerMissionFightWorker(self.voyager)
        self.s = PlayerSkillCooldownWorker(self.voyager)
        self.a = PlayerAttackWorker(self.voyager)

        self.workers = []

    def init(self):
        self.running = True
        self.workers = [self.f, self.s, self.a]
        for s in self.workers:
            s.start()

    def _run(self):
        cls = self.voyager.recogbot.detect()

        # if self.count % 5 == 0:
        #     # 装备修理
        #     if not self.voyager.game.repaired and cls['bag'][0] and cls['bag'][2] < 200:
        #         self.voyager.game.repair_and_sale(cls['bag'])
        # else:
        #     self.voyager.game.repaired = True
        if not self.voyager.game.repaired and cls['bag'][0] and cls['bag'][2] < 200:
            self.voyager.game.repair_and_sale(cls['bag'])

        # 出现游戏教程，对话时按Esc跳过
        if cls['skip'][0] or cls['tutorial'][0]:
            self.voyager.game.esc()

        # 地下城里面点击下个任务
        if self.voyager.game.repaired and cls['next'][0]:
            # self.count += 1
            self.voyager.game.next(cls['next'])

        # 自动装备
        if self.voyager.recogbot.equip():
            self.voyager.game.equip()

        if self.voyager.recogbot.confirm():
            self.voyager.game.confirm()

        # 战斗奖励
        if self.voyager.recogbot.reward():
            print("【目标检测】战斗奖励，战斗结束!")
            self.voyager.game.reward()

        # 返回
        if self.voyager.recogbot.back():
            self.voyager.game.back()

        # 死亡
        if self.voyager.recogbot.dead():
            self.voyager.game.revival()

        # 疲劳值不足
        if self.voyager.recogbot.insufficient_balance_mission():
            self.voyager.game.agency_mission_finish()
            self.voyager.player.over_fatigued()
            self.trigger.emit(str('stop'))

        if self.voyager.recogbot.next_agency():
            self.voyager.game.next_agency()

        if self.voyager.recogbot.next_agency_confirm():
            self.voyager.game.next_agency_confirm()

        # 酒馆接受任务
        if self.voyager.recogbot.agency_mission_get():
            self.voyager.game.agency_mission_get()

        # 天界任务领取
        if self.voyager.recogbot.heaven_mission_receive():
            self.voyager.game.heaven_mission_receive()

        # 暗黑城卡住
        if self.voyager.recogbot.black_town_stuck():
            print('暗黑城脱困')
            self.voyager.game.out_stuck('down')

        # 天界卡住
        if self.voyager.recogbot.heaven_stuck():
            print('天界脱困')
            self.voyager.game.out_stuck('right')

        # 没有主线任务了，去打怪升级
        if self.voyager.recogbot.agency_mission_confirm():
            self.voyager.game.agency_mission_confirm()

        # 没有主线任务，再次挑战
        if self.voyager.recogbot.next_agency_none():
            self.voyager.game.replay_agency()

    def run(self):
        self.init()
        print("【自动升级】主线任务开始执行")
        while self.running:
            self._run()

    def stop(self):
        print("【自动升级】主线任务停止执行")
        for s in self.workers:
            s.stop()
        self.running = False
