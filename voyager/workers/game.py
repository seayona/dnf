import time

from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from voyager.game import Game, Player
from voyager.recognition import Recogbot


class GameWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, game, recogbot):
        # 初始化函数，默认
        super(GameWorker, self).__init__()
        self.game = game
        self.recogbot = recogbot

    def _run(self):

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

        # 疲劳值不足，打完深渊的时候
        if self.recogbot.insufficient_balance_demon():
            print("【雪山】疲劳值不足，打完深渊的时候")
            self.game.snow_mountain_finish()
            self.trigger.emit('on_striver_completed')

        # 疲劳值不足
        if self.recogbot.insufficient_balance():
            print("【雪山】疲劳值不足")
            self.game.snow_mountain_finish()
            self.trigger.emit('on_striver_completed')

    def run(self):
        print("【雪山】雪山开始执行")
        while True:
            self._run()

    def stop(self):
        print("【工作线程】雪山停止执行")
        self.terminate()
