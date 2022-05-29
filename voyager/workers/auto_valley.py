import time

from PyQt5.QtCore import QThread, pyqtSignal

from .auto_worker import AutoWorker
from .worker_valley import ValleyWorker


class AutoValleyWorker(AutoWorker):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super().__init__(voyager, 'Valley')
        self.running = False

        self.v = ValleyWorker(self.voyager)
        self.v.trigger.connect(self.finish)

        self.workers = [self.v]

    def init(self):
        self.running = True
        self.reset()

    # 线程入口
    def run(self):
        self.init()
        print("【一键溪谷】自动溪谷开始执行", int(QThread.currentThreadId()))
        while self.running:
            self.continuous_run()
            time.sleep(5)

    # 停止线程
    def stop(self):
        print("【一键溪谷】自动溪谷停止执行")
        for s in self.workers:
            s.stop()
        if self.worker is not None:
            self.worker.stop()
        self.running = False
