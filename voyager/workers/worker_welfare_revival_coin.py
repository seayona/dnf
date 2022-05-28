import time

from PyQt5.QtCore import QThread, pyqtSignal


class WelfareRevivalCoinWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareRevivalCoinWorker, self).__init__()
        self.game = voyager.game
        self.recogbot = voyager.recogbot
        self.player = voyager.player

    def _run(self):
        # 复活币领取成功
        pass

    def run(self):
        print("【自动福利】复活币福利开始执行", int(QThread.currentThreadId()))
        self.trigger.emit(str('stop'))
        while True:
            self._run()
            time.sleep(1)

    def stop(self):
        print("【自动福利】复活币福利执行结束")
        self.terminate()
