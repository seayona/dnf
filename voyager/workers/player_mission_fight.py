import time

from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QEventLoop

from voyager.game import Game, Player
from voyager.recognition import Recogbot


class PlayerMissionFightWorker(QThread):
    # 定义一个信号ex
    trigger = pyqtSignal(str)

    def __init__(self, game, recogbot, player):
        # 初始化函数，默认
        super(PlayerMissionFightWorker, self).__init__()
        self.game = game
        self.recogbot = recogbot
        self.player = player

    def _cooldown(self):
        print("【战斗】技能计时器")
        self.player.cooldown()

    def _run(self):
        monster, lion, boss, door = self.recogbot.detect()

        if not self.recogbot.door():
            print("【目标检测】门没开，无脑输出")
            self.player.cast()

    def run(self):
        print("【战斗】战斗开始执行")
        print('thread id', int(QThread.currentThreadId()))
        while True:
            self._run()

    def stop(self):
        print("【战斗】战斗停止执行")
        self.terminate()
