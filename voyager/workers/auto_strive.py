from PyQt5.QtCore import QThread, pyqtSignal

from .auto_worker import AutoWorker

from .worker_valley import ValleyWorker
from .worker_welfare import WelfareWorker
from .worker_snowmountain import GameWorker


class AutoStriveWorker(AutoWorker):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super().__init__(voyager, 'Strive')
        self.append(ValleyWorker(self.voyager))
        self.append(WelfareWorker(self.voyager))
        self.append(GameWorker(self.voyager))

    # 线程入口
    def run(self):
        print("【一键搬砖】自动搬砖开始执行", int(QThread.currentThreadId()))
        while True:
            self.continuous_run()

    # 停止线程
    def stop(self):
        print("【一键搬砖】自动搬砖停止执行")
        for s in self.workers_queue:
            s.stop()
        self.terminate()
