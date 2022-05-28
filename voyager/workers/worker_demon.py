
from PyQt5.QtCore import QThread, pyqtSignal, QTimer


class DemonWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        # 初始化函数，默认
        super(DemonWorker, self).__init__()
        self.game = voyager.game
        self.recogbot = voyager.recogbot

    def _run(self):
        pass

    def run(self):
        print("【自动深渊】自动深渊开始执行")
        while True:
            self._run()

    def stop(self):
        print("【自动深渊】自动深渊停止执行")
        self.terminate()
