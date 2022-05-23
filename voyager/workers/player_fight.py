import time

from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QEventLoop

from voyager.game import Game, Player
from voyager.recognition import Recogbot


class PlayerFightWorker(QThread):
    # 定义一个信号ex
    trigger = pyqtSignal(str)

    def __init__(self, game, recogbot, player):
        # 初始化函数，默认
        super(PlayerFightWorker, self).__init__()
        self.game = game
        self.recogbot = recogbot
        self.player = player

    def _run(self):
        monster, lion, boss, door = self.recogbot.detect()
        lion_alive = self.game.lionAlive

        # 发现狮子头入口
        if lion_alive and door and self.recogbot.lion_entry2():
            print("【战斗】发现狮子头入口2!")
            self.player.stand()
            self.player.right()

        # 释放技能
        if monster:
            print("【战斗】还有小可爱活着")
            self.player.cast()

        # 发现狮子头入口
        if lion_alive and door and self.recogbot.lion_entry1():
            print("【战斗】发现狮子头入口1!")
            self.player.stand()
            self.player.right()

        # 释放觉醒
        if boss:
            print("【战斗】发现Boss!")
            self.player.finisher()

        # 发现狮子头入口
        if lion_alive and door and self.recogbot.lion_entry():
            print("【战斗】发现狮子头入口!")
            self.player.stand()
            self.player.right()

        # 狮子头
        if lion:
            print("【战斗】发现狮子头!")
            self.game.lion_clear()
            self.player.attack()
            self.player.finisher()

    def run(self):
        print("【战斗】战斗开始执行")
        while True:
            self._run()

    def stop(self):
        print("【战斗】战斗停止执行")
        self.terminate()
