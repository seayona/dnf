import time

from PyQt5.QtCore import QThread, pyqtSignal

from voyager.game import Player


class PlayerAttackWorker(QThread):
    # 定义一个信号ex
    trigger = pyqtSignal(str)

    def __init__(self,player):
        # 初始化函数，默认
        super(PlayerAttackWorker, self).__init__()
        self.player = player

    def _run(self):
        print('【自动攻击】Thread', int(QThread.currentThreadId()))
        self.player.attack()

    def run(self):
        print("【自动攻击】自动攻击开始执行")
        while True:
            self._run()
            time.sleep(3.2)

    def stop(self):
        print("【自动攻击】自动攻击停止执行")
        self.player.stand()
        self.terminate()
