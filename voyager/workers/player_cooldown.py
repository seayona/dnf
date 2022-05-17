import time

from PyQt5.QtCore import QThread, pyqtSignal

from voyager.game import Player


class PlayerSkillCooldownWorker(QThread):
    # 定义一个信号ex
    trigger = pyqtSignal(str)

    def __init__(self, player):
        # 初始化函数，默认
        super(PlayerSkillCooldownWorker, self).__init__()
        self.player = player

    def _run(self):
        self.player.cooldown()

    def run(self):
        print("【技能计时】技能计时开始执行")
        while True:
            self._run()
            time.sleep(1)

    def stop(self):
        print("【技能计时】技能计时停止执行")
        self.terminate()
