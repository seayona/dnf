import time

from PyQt5.QtCore import QThread, pyqtSignal

from .auto_worker import AutoWorker

from .worker_daily_valley import ValleyWorker
from .worker_welfare import WelfareWorker
from .worker_agency_mission import AgencyMissionWorker


class AutoLevelUpWorker(AutoWorker):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(AutoLevelUpWorker, self).__init__(voyager, 'LevelUp')
        self.running = False

        self.v = ValleyWorker(self.voyager)
        self.v.trigger.connect(self.finish)

        self.w = WelfareWorker(self.voyager)
        self.w.trigger.connect(self.finish)

        self.a = AgencyMissionWorker(self.voyager)
        self.a.trigger.connect(self.finish)

        self.workers = [self.w, self.v, self.a]

    def init(self):
        self.running = True
        self.reset()

    # 线程入口
    def run(self):
        self.init()
        print("【一键升级】一键升级开始执行", int(QThread.currentThreadId()))
        while self.running:
            self.continuous_run()
            time.sleep(5)

    # 停止线程和线程唤起的其他线程
    def stop(self):
        print("【一键升级】一键升级停止执行")
        for s in self.workers:
            s.stop()
        if self.worker is not None:
            self.worker.stop()
        self.running = False
