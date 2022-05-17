from PyQt5.QtCore import QThread, QTimer


class PlayerAttackTimer(object):
    def __init__(self, player):
        self.timer = QTimer()
        self.timer.timeout.connect(self._run)
        self.player = player

    def _run(self):
        print('【自动攻击】Thread', int(QThread.currentThreadId()))
        self.player.attack()

    def start(self):
        print("【自动攻击】自动攻击开始执行")
        self.timer.start(3200)

    def stop(self):
        print("【自动攻击】自动攻击停止执行")
        self.player.stand()
        self.timer.stop()
