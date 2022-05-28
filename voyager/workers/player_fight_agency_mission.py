from PyQt5.QtCore import QThread, pyqtSignal



class PlayerMissionFightWorker(QThread):
    # 定义一个信号ex
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        # 初始化函数，默认
        super(PlayerMissionFightWorker, self).__init__()
        self.game = voyager.game
        self.recogbot = voyager.recogbot
        self.player = voyager.player

    def _run(self):
        cls = self.recogbot.detect()
        if cls['combo'][0]:
            print("【目标检测】还有小可爱活着，无脑输出")
            self.player.cast()

    def run(self):
        print("【战斗】战斗开始执行")
        while True:
            self._run()

    def stop(self):
        print("【战斗】战斗停止执行")
        self.terminate()
