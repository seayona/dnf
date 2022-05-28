from PyQt5.QtCore import QThread, pyqtSignal

from .worker_welfare_revival_coin import WelfareRevivalCoinWorker
from .worker_welfare_union import WelfareUnionWorker


class WelfareWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareWorker, self).__init__()
        self.voyager = voyager
        self.game = voyager.game
        self.recogbot = voyager.recogbot

        self.worker = None
        self.working = False

        # 公会签到
        w = WelfareUnionWorker(self.voyager)
        w.trigger.connect(self._finish)

        # 商城复活币
        r = WelfareRevivalCoinWorker(self.voyager)
        r.trigger.connect(self._finish)

        # 每日

        # 添加到队列
        self.workers_queue = [w, r]

    def _finish(self):
        print(f"{self.worker.__class__.__name__}执行结束")
        self.worker.stop()
        self.working = False

    def _run(self):
        if not self.working and len(self.workers_queue) > 0:
            self.worker = self.workers_queue.pop()
            self.worker.start()
            print(f"{self.worker.__class__.__name__}开始执行")
            self.working = True

        if not self.working and len(self.workers_queue) == 0:
            self.trigger.emit(str('stop'))

    def run(self):
        print("【探索者】福利领取开始执行", int(QThread.currentThreadId()))
        while True:
            self._run()

    def stop(self):
        print("【探索者】福利领取停止执行")
        self.terminate()
