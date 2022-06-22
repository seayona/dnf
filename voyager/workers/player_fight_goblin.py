from PyQt5.QtCore import QThread, pyqtSignal
import time


class GoblinFightWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(GoblinFightWorker, self).__init__()
        self.voyager = voyager
        self.running = False

    def init(self):
        self.running = True

    def _run(self):
        cls = self.voyager.recogbot.detect()
        if cls['boss'][0]:
            self.voyager.player.cast()
            self._finisher()

    def _finisher(self):
        if self.voyager.recogbot.skill(self.voyager.player.awake['icon']):
            self.voyager.player.finisher()

    def run(self):
        self.init()
        print("【哥布林】战斗开始执行")
        while self.running:
            self._run()
            time.sleep(2)

    def stop(self):
        print("【哥布林】战斗停止执行")
        self.running = False
