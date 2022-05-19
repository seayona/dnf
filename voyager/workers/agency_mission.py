from PyQt5.QtCore import QThread, pyqtSignal

from voyager.game import Game, Player
from voyager.recognition import Recogbot


class AgencyMissionWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, game: Game, recogbot: Recogbot, player: Player):
        # 初始化函数，默认
        super(AgencyMissionWorker, self).__init__()
        self.game = game
        self.recogbot = recogbot
        self.player = player

    def _run(self):
        # 装备修理
        if not self.game.repaired and self.recogbot.bag():
            self.game.repair()

        # 装备分解
        if not self.game.saled and self.recogbot.bag():
            self.game.sale()

        if self.recogbot.talk():
            self.game.talk_skip()

        if self.recogbot.confirm():
            self.game.confirm()

        # 战斗奖励
        if self.recogbot.reward():
            print("【目标检测】战斗奖励，战斗结束!")
            self.game.reward()

        # 返回
        if self.recogbot.back():
            self.game.back()

        # 自动装备
        if self.recogbot.equip():
            self.game.equip()

        # 点击关闭
        if self.recogbot.click_close():
            self.game.click_close()

        # 死亡
        if self.recogbot.dead():
            self.game.revival()

        # 疲劳值不足
        if self.recogbot.insufficient_balance_mission():
            self.game.agency_mission_finish()
            self.trigger.emit(str('stop'))

        if self.game.repaired and self.game.saled and self.recogbot.next():
            self.game.next()

        if self.recogbot.next_agency():
            self.game.next_agency()

        if self.recogbot.next_agency_confirm():
            self.game.next_agency_confirm()

        if self.recogbot.sylia():
            self.game.agency_skip()

        # 酒馆接受任务
        if self.recogbot.agency_mission_get():
            self.game.agency_mission_get()

        # 没有主线任务了，去打怪升级
        if self.recogbot.agency_mission_confirm():
            self.game.agency_mission_confirm()

        # 没有主线任务，再次挑战
        if self.recogbot.next_agency_none():
            self.game.replay_agency()

    def run(self):
        print("【工作线程】主线任务开始执行")
        while True:
            self._run()

    def stop(self):
        print("【工作线程】主线任务停止执行")
        self.terminate()
