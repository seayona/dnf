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
        self.game = voyager.game
        self.recogbot = voyager.recogbot
        self.player = voyager.player
        self.count = 0

        f = PlayerMissionFightWorker(self.voyager)
        s = PlayerSkillCooldownWorker(self.voyager)
        a = PlayerAttackWorker(self.voyager)

        # 装配到works
        self.workers = [f, s, a]

    def _run(self):
        cls = self.recogbot.detect()

        # if self.count % 5 == 0:
        #     # 装备修理
        #     if not self.game.repaired and cls['bag'][0] and cls['bag'][2] < 200:
        #         self.game.repair_and_sale(cls['bag'])
        # else:
        #     self.game.repaired = True
        if not self.game.repaired and cls['bag'][0] and cls['bag'][2] < 200:
            self.game.repair_and_sale(cls['bag'])

        # 出现游戏教程，对话时按Esc跳过
        if cls['skip'][0] or cls['tutorial'][0]:
            self.game.esc()

        # 地下城里面点击下个任务
        if self.game.repaired and cls['next'][0]:
            self.count += 1
            self.game.next(cls['next'])

        # 自动装备
        if self.recogbot.equip():
            self.game.equip()

        if self.recogbot.confirm():
            self.game.confirm()

        # 战斗奖励
        if self.recogbot.reward():
            print("【目标检测】战斗奖励，战斗结束!")
            self.game.reward()

        # 返回
        if self.recogbot.back():
            self.game.back()

        # 死亡
        if self.recogbot.dead():
            self.game.revival()

        # 疲劳值不足
        if self.recogbot.insufficient_balance_mission():
            self.game.agency_mission_finish()
            self.player.over_fatigued()
            self.trigger.emit(str('stop'))

        if self.recogbot.next_agency():
            self.game.next_agency()

        if self.recogbot.next_agency_confirm():
            self.game.next_agency_confirm()

        # 酒馆接受任务
        if self.recogbot.agency_mission_get():
            self.game.agency_mission_get()

        # 天界任务领取
        if self.recogbot.heaven_mission_receive():
            self.game.heaven_mission_receive()

        # 暗黑城卡住
        if self.recogbot.black_town_stuck():
            print('暗黑城脱困')
            self.game.out_stuck('down')

        # 天界卡住
        if self.recogbot.heaven_stuck():
            print('天界脱困')
            self.game.out_stuck('right')

        # 没有主线任务了，去打怪升级
        if self.recogbot.agency_mission_confirm():
            self.game.agency_mission_confirm()

        # 没有主线任务，再次挑战
        if self.recogbot.next_agency_none():
            self.game.replay_agency()

    def run(self):
        print("【自动升级】主线任务开始执行")
        for s in self.workers:
            s.start()
        while True:
            self._run()

    def stop(self):
        print("【自动升级】主线任务停止执行")
        for s in self.workers:
            s.stop()
        self.terminate()
