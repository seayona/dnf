import time

from PyQt5.QtCore import QThread, QTimer, pyqtSignal

from voyager.recognition import Recogbot


class PlayerAttackWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(PlayerAttackWorker, self).__init__()
        self.voyager = voyager
        self.running = False

    def init(self):
        self.running = True

    def _run(self):
        for key in self.voyager.player.buff.keys():
            if self.voyager.recogbot.buff(key):
                self.voyager.player.release_buff(key)

        self.voyager.player.attack()

    def run(self):
        self.init()
        print("【自动攻击】战斗开始执行")
        while self.running:
            self._run()
            time.sleep(3.2)

    def stop(self):
        print("【自动攻击】战斗停止执行")
        self.running = False
