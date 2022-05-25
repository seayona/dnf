
from PyQt5.QtCore import QThread, pyqtSignal

class PlayerFightWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, game, recogbot, player):
        # 初始化函数，默认
        super(PlayerFightWorker, self).__init__()
        self.game = game
        self.recogbot = recogbot
        self.player = player

    def _run(self):
        cls = self.recogbot.detect()

        # 发现狮子头入口
        if self.game.lionAlive and cls['door'][0] and cls['lion_entry'][0]:
            print("【战斗】发现狮子头入口!")
            self.player.stand()
            self.player.right()

        # 释放技能
        if cls['combo'][0]:
            print("【战斗】还有小可爱活着")
            self.player.cast()

        # 释放觉醒
        if cls['boss'][0]:
            print("【战斗】发现Boss!")
            self.player.finisher()

        # 狮子头
        if cls['lion'][0]:
            print("【战斗】发现狮子头!")
            self.game.lion_clear()
            self.player.attack()
            self.player.finisher()

    def run(self):
        print("【战斗】战斗开始执行")
        while True:
            self._run()

    def stop(self):
        print("【战斗】战斗停止执行")
        self.terminate()
