import time

from PyQt5.QtCore import QThread, pyqtSignal, QTimer


class DemonWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        # 初始化函数，默认
        super(DemonWorker, self).__init__()
        self.running = False
        self.workers = []

    def init(self):
        self.running = True

    def _run(self):
        self.trigger.emit(self.__class__.__name__)

    def run(self):
        self.init()
        print("【自动深渊】自动深渊开始执行")
        while self.running:
            self._run()
            time.sleep(0.5)

    def stop(self):
        print("【自动深渊】自动深渊停止执行")
        for s in self.workers:
            s.stop()
        self.running = False
