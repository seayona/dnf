import time

from PyQt5.QtCore import QThread, pyqtSignal, QTimer

from voyager.game import Player


class PlayerSkillCooldownTimer(object):

    def __init__(self, player):
        self.timer = QTimer()
        self.timer.timeout.connect(self._run)
        self.player = player

    def _run(self):
        self.player.cooldown()

    def start(self):
        print("【技能计时】技能计时开始执行")
        self.timer.start(1000)

    def stop(self):
        print("【技能计时】技能计时停止执行")
        self.timer.stop()
