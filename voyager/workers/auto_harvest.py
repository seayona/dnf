import time

from PyQt5.QtCore import QThread, pyqtSignal

from .worker_welfare_mail_receive import WelfareMailReceive
from .auto_worker import AutoWorker

from .woker_collect_precious import CollectPrecious
from .worker_welfare_union import WelfareUnionWorker
from .woker_use_consumable import UseConsumable


class AutoHarvestWorker(AutoWorker):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super().__init__(voyager, 'Harvest')
        self.running = False
        self.voyager = voyager

        self.c = CollectPrecious(self.voyager)
        self.c.trigger.connect(self.finish)

        self.m = WelfareMailReceive(self.voyager)
        self.m.trigger.connect(self.finish)

        self.u = WelfareUnionWorker(self.voyager)
        self.u.trigger.connect(self.finish)

        self.a = UseConsumable(self.voyager)
        self.a.trigger.connect(self.finish)

        self.workers = [self.c, self.a, self.m, self.u]

    def init(self):
        self.running = True
        self.reset()

    # 线程入口
    def run(self):
        self.init()
        print("【一键福利】一键福利开始执行", int(QThread.currentThreadId()))
        while self.running:
            self.continuous_run()
            time.sleep(1.5)

    # 停止线程
    def stop(self):
        print("【一键福利】一键福利停止执行")
        for s in self.workers:
            s.stop()
        if self.worker is not None:
            self.worker.stop()
        self.running = False
