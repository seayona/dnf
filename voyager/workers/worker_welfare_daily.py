import time

from PyQt5.QtCore import QThread, pyqtSignal


class WelfareDailyWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareDailyWorker, self).__init__()
        self.voyager = voyager
        self.running = False

    def init(self):
        self.running = True

    def _run(self):
        if True:
            self.trigger.emit(str('stop'))

    def run(self):
        self.init()
        self._init_box()
        print("【每日福利】每日福利开始执行", int(QThread.currentThreadId()))
        while self.running:
            self._run()

    def stop(self):
        print("【每日福利】每日福利开始执行")
        self.running = False
