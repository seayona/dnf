import time

from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from voyager.game import Player


class PlayerSkillCooldownWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(Player)

    def __init__(self, player: Player):
        super(PlayerSkillCooldownWorker, self).__init__()
        self.player = player

    def _run(self):
        self.player.cooldown()

    def run(self):
        print("【技能计时器】技能计时器开始执行")
        while True:
            self._run()
            time.sleep(1)

    def stop(self):
        print("【技能计时】技能计时停止执行")
        self.terminate()
