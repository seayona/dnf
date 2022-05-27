from PyQt5.QtCore import QThread, pyqtSignal


class WelfareGuild(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, game, recogbot, ):
        super(WelfareGuild, self).__init__()

        self.game = game
        self.recogbot = recogbot
        self.signed = 0

    def _run(self):

        if self.signed == 2:
            self.trigger.emit(str('stop'))

        if self.recogbot.town() and not self.signed == 2:
            self.game.guild_sign()
            self.signed = 1

        box, gold = self.recogbot.guild_signed()
        if not box and gold and self.signed == 1:
            self.signed = 2

        if box and not self.recogbot.town():
            self.game.guild_box()
            self.signed = 1

    def run(self):
        print("【探索者】公会福利开始执行", int(QThread.currentThreadId()))
        self.signed = 0
        while True:
            self._run()

    def stop(self):
        print("【探索者】公会福利开始执行")
        self.terminate()
