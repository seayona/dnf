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

    def _finish(self, params):
        print("任务执行结束", params)
        self.worker.stop()
        self.working = False
        self.worker = None

    def _run(self):
        if not self.working and len(self.workers) > 0:
            self.worker = self.workers.pop()
            self.worker.start()
            self.working = True

        if not self.working and len(self.workers) == 0:
            self.voyager.game.back()
            self.trigger.emit(str('stop'))

    def run(self):
        self.init()
        print("【探索者】福利领取开始执行")
        while self.running:
            self._run()
            self.sleep(1)

    def stop(self):
        print("【探索者】福利领取停止执行")
        print(self.worker)
        for s in self.workers:
            s.stop()
        if self.worker is not None:
            self.worker.stop()
        self.running = False
