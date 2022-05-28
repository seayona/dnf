import time

from PyQt5.QtCore import QThread, pyqtSignal


from .auto_worker import AutoWorker
from .worker_valley import ValleyWorker

class AutoValleyWorker(AutoWorker):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super().__init__(voyager, 'Valley')
        self.append(ValleyWorker(self.voyager))

    # 线程入口
    def run(self):
        print("【一键溪谷】自动溪谷开始执行", int(QThread.currentThreadId()))
        while True:
            self.continuous_run()
            time.sleep(5)

    # 停止线程
    def stop(self):
        print("【一键溪谷】自动溪谷停止执行")
        for s in self.workers_queue:
            s.stop()
        self.terminate()
