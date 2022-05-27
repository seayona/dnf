from PyQt5.QtCore import QThread, pyqtSignal


class WelfareGuild(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, game, recogbot, ):
        super(WelfareGuild, self).__init__()

        self.game = game
        self.recogbot = recogbot

    def _run(self):
        if self.recogbot.town():
            self.game.guild_welfare()

        box, gold = self.recogbot.guild_signed()
        if not box and gold:
            self.trigger.emit(str('stop'))
            return

        if box:
            self.game.guild_box()


    def run(self):
        print("【探索者】公会福利开始执行", int(QThread.currentThreadId()))
        while True:
            self._run()

    def stop(self):
        print("【探索者】公会福利开始执行")
        self.terminate()
