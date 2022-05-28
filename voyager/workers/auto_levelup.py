import time

from PyQt5.QtCore import QThread, pyqtSignal

from .auto_worker import AutoWorker

from .worker_valley import ValleyWorker
from .worker_welfare import WelfareWorker
from .worker_agency_mission import AgencyMissionWorker


class AutoLevelUpWorker(AutoWorker):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(AutoLevelUpWorker, self).__init__(voyager, 'LevelUp')

        self.append(ValleyWorker(self.voyager))
        self.append(WelfareWorker(self.voyager))
        self.append(AgencyMissionWorker(self.voyager))

    # 线程入口
    def run(self):
        print("【一键升级】一键升级开始执行", int(QThread.currentThreadId()))
        while True:
            self.continuous_run()
            time.sleep(5)

    # 停止线程和线程唤起的其他线程
    def stop(self):
        print("【一键升级】一键升级停止执行")
        for s in self.workers_queue:
            s.stop()
        self.terminate()
