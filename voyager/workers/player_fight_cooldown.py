import time

from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from voyager.game import Player


class PlayerSkillCooldownWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(PlayerSkillCooldownWorker, self).__init__()
        self.voyager = voyager
        self.running = False

    def init(self):
        self.running = True

    def _run(self):
        self.voyager.player.cooldown()

    def run(self):
        self.init()
        print("【技能计时器】技能计时器开始执行")
        while self.running:
            self._run()
            time.sleep(1)

    def stop(self):
        print("【技能计时】技能计时停止执行")
        self.running = False
