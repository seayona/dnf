import time

from PyQt5.QtCore import QThread, pyqtSignal

from .auto_worker import AutoWorker

from .woker_duel import DuelWork


class AutoDuelWorker(AutoWorker):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super().__init__(voyager, 'Duel')
        self.running = False
        self.voyager = voyager

        self.d = DuelWork(self.voyager)
        self.d.trigger.connect(self.finish)
        self.workers = [self.d]

    def init(self):
        self.running = True
        self.reset()

    # 线程入口
    def run(self):
        self.init()
        print("【一键决斗】一键决斗开始执行", int(QThread.currentThreadId()))
        while self.running:
            self.continuous_run()
            time.sleep(1.5)

    # 停止线程
    def stop(self):
        print("【一键决斗】一键决斗停止执行")
        for s in self.workers:
            s.stop()
        if self.worker is not None:
            self.worker.stop()
        self.running = False
