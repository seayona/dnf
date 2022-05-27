import time

from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from voyager.game import Game, Player
from voyager.recognition import Recogbot


class ValleyWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, game, recogbot):
        # 初始化函数，默认
        super(ValleyWorker, self).__init__()
        self.game = game
        self.recogbot = recogbot

    def _run(self):

        if self.recogbot.daliy_valley_completed():
            print("【目标检测】祥瑞溪谷已刷完！")
            self.game.esc()
            self.trigger.emit(str('stop'))
            return

        # 发现祥瑞溪谷入口
        if self.recogbot.daily_valley():
            print("【目标检测】发现祥瑞溪谷入口！")
            self.game.valley_fight()

        # 溪谷再次挑战
        if self.recogbot.replay():
            self.game.valley_replay()

        # 死亡
        if self.recogbot.dead():
            self.game.revival()

        # 返回日常界面
        if self.recogbot.daily_valley_town():
            self.game.valley_town()

        if self.recogbot.town():
            self.game.valley_start()

    def run(self):
        print("【工作线程】祥瑞溪谷开始执行")
        while True:
            self._run()

    def stop(self):
        print("【工作线程】祥瑞溪谷停止执行")
        self.terminate()
