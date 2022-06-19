import time

from PyQt5.QtCore import QThread, pyqtSignal

from .auto_worker import AutoWorker

from .woker_collect_precious import CollectPrecious


class AutoHarvestWorker(AutoWorker):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super().__init__(voyager, 'Harvest')
        self.running = False
        self.voyager = voyager

        self.c = CollectPrecious(self.voyager)
        self.c.trigger.connect(self.finish)
        self.workers = [self.c]

    def init(self):
        self.running = True
        self.reset()

    # 线程入口
    def run(self):
        self.init()
        print("【一键福利】一键福利开始执行", int(QThread.currentThreadId()))
        while self.running:
            self.continuous_run()
            time.sleep(5)

    # 停止线程
    def stop(self):
        print("【一键福利】一键福利停止执行")
        for s in self.workers:
            s.stop()
        if self.worker is not None:
            self.worker.stop()
        self.running = False
