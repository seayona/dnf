from PyQt5.QtCore import QThread, pyqtSignal


class PlayerMissionFightWorker(QThread):
    # 定义一个信号ex
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        # 初始化函数，默认
        super(PlayerMissionFightWorker, self).__init__()
        self.voyager = voyager
        self.running = False

    def init(self):
        self.running = True

    def _run(self):
        cls = self.voyager.recogbot.detect()
        if (cls['combo'][0] and cls['avatar'][0]) or (cls['combo'][0] and cls['boss'][0]):
            print("【目标检测】还有小可爱活着，无脑输出")
            self.voyager.player.cast()
            self.voyager.matric.combo(cls['combo'])

    def run(self):
        self.init()
        print("【战斗】战斗开始执行")
        while self.running:
            self._run()

    def stop(self):
        print("【战斗】战斗停止执行")
        self.running = False
