import time

from PyQt5.QtCore import QThread, pyqtSignal

from .worker_welfare_revival_coin import WelfareRevivalCoinWorker
from .worker_welfare_union import WelfareUnionWorker


class WelfareWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareWorker, self).__init__()
        self.voyager = voyager
        self.running = False
        self.working = False
        self.worker = None
        self.workers = []

        # 公会签到
        self.w = WelfareUnionWorker(self.voyager)
        self.w.trigger.connect(self._finish)

        # 商城复活币
        self.r = WelfareRevivalCoinWorker(self.voyager)
        self.r.trigger.connect(self._finish)

    def init(self):
        self.running = True
        self.worker = None
        self.working = False
        # 每日

        # 添加到队列
        self.workers = [self.w, self.r]

    def _finish(self, args):
        if self.worker is None:
            print(f"【一键福利】意外的线程结束：{args}")
            return

        if self.worker.__class__.__name__ == args:
            print("【一键福利】任务执行结束", args)
            self.worker.stop()
            self.worker = None
            self.working = False

    def _run(self):
        if not self.working and len(self.workers) > 0:
            # 等待上个任务完全停止
            self.sleep(10)
            self.worker = self.workers.pop()
            self.worker.start()
            self.working = True

        if not self.working and len(self.workers) == 0:
            self.voyager.matric.heartbeat()
            self.trigger.emit(self.__class__.__name__)

    def run(self):
        self.init()
        print("【一键福利】福利领取开始执行")
        while self.running:
            self._run()
            self.sleep(1)

    def stop(self):
        print("【一键福利】福利领取停止执行")
        print(self.worker)
        for s in self.workers:
            s.stop()
        if self.worker is not None:
            self.worker.stop()
        self.running = False
