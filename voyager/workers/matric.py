import datetime
import time

from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from voyager.game import Player


class MatricWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(MatricWorker, self).__init__()
        self.voyager = voyager
        self.running = False
        self.sleep_second = 10

    def init(self):
        self.running = True
        self.sleep_second = 10

    def _run(self):
        if len(self.voyager.matric.combos.data()) == 0:
            return
        diff = (datetime.datetime.now() - self.voyager.matric.combos.data()[-1][0])
        if diff.seconds > 60 * 3:
            self.voyager.notification.send(f"【{self.voyager.player.name}】Must return to work,Now!")
            if self.sleep_second > 300:
                self.sleep_second = 300
            else:
                self.sleep_second += 60
        else:
            self.sleep_second = 10

    def run(self):
        self.init()
        print("【监控告警】监控告警开始执行")
        while self.running:
            self._run()
            time.sleep(self.sleep_second)

    def stop(self):
        print("【监控告警】监控告警停止执行")
        self.running = False
