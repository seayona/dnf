import time

from PyQt5.QtCore import QThread, pyqtSignal


class WelfareRevivalCoinWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareRevivalCoinWorker, self).__init__()
        self.voyager = voyager
        self.running = False

    def init(self):
        self.running = True

    def _run(self):

        if True:
            print("【复活币福利】复活币领取完成")
            # 复活币领取成功
            self.trigger.emit('stop')

    def run(self):
        self.init()
        print("【自动福利】复活币福利开始执行")
        while self.running:
            self._run()
            self.sleep(1)

    def stop(self):
        print("【自动福利】复活币福利执行结束")
        self.running = False
