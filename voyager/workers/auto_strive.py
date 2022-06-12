import time

from PyQt5.QtCore import QThread, pyqtSignal

from .auto_worker import AutoWorker

from .worker_daily_valley import ValleyWorker
from .worker_welfare import WelfareWorker
from .worker_snowmountain import GameWorker
from .worker_daily_south import SouthWorker
from .worker_daily_goblin import GoblinWorker
from .worker_daily_carbon import CarbonWorker


class AutoStriveWorker(AutoWorker):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super().__init__(voyager, 'Strive')
        self.running = False

        self.v = ValleyWorker(self.voyager)
        self.v.trigger.connect(self.finish)

        self.w = WelfareWorker(self.voyager)
        self.w.trigger.connect(self.finish)

        self.a = GameWorker(self.voyager)
        self.a.trigger.connect(self.finish)

        self.s = SouthWorker(self.voyager)
        self.s.trigger.connect(self.finish)

        self.g = GoblinWorker(self.voyager)
        self.g.trigger.connect(self.finish)

        self.c = CarbonWorker(self.voyager)
        self.c.trigger.connect(self.finish)

        self.workers = [self.c, self.s, self.g, self.v, self.w, self.a]

    def init(self):
        self.running = True
        self.reset()

    # 线程入口
    def run(self):
        self.init()
        print("【一键搬砖】自动搬砖开始执行", int(QThread.currentThreadId()))
        while self.running:
            self.continuous_run()
            time.sleep(1.5)

    # 停止线程
    def stop(self):
        print("【一键搬砖】自动搬砖停止执行")
        for s in self.workers:
            s.stop()
        if self.worker is not None:
            self.worker.stop()
        self.running = False
