import time

from PyQt5.QtCore import QThread, QTimer, pyqtSignal

from voyager.recognition import Recogbot


class PlayerAttackWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(PlayerAttackWorker, self).__init__()
        self.player = voyager.player
        self.recogbot = voyager.recogbot

    def _run(self):
        print('【自动攻击】Thread', int(QThread.currentThreadId()))
        for key in self.player.buff.keys():
            if self.recogbot.buff(key):
                self.player.release_buff(key)

        self.player.attack()

    def run(self):
        print("【自动攻击】战斗开始执行")
        while True:
            self._run()
            time.sleep(3.2)

    def stop(self):
        print("【自动攻击】战斗停止执行")
        self.terminate()

    # def watch(self, player):
    #     self.player = player

    # def start(self):
    #     print("【自动攻击】自动攻击开始执行")
    #     self.timer.start(3200)
    #
    # def stop(self):
    #     print("【自动攻击】自动攻击停止执行")
    #     self.player.stand()
    #     self.timer.stop()
