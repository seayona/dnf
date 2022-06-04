import time

from PyQt5.QtCore import QThread, pyqtSignal


class WelfareMailReceive(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareMailReceive, self).__init__()
        self.voyager = voyager
        self.running = False

    def init(self):
        self.running = True

    def _run(self):
        if self.voyager.recogbot.town() and self.voyager.player.welfare['mail']:
            self.trigger.emit(str('stop'))

        if self.voyager.recogbot.town() and not self.voyager.player.welfare['mail']:
            self.voyager.game.goto_mail()

        if self.voyager.recogbot.mail_receive():
            self.voyager.game.mail_receive()

        if self.voyager.recogbot.mail_received():
            self.voyager.player.over_welfare('mail')
            self.voyager.game.back()

        # 领取后在城镇stop
        if True:
            self.trigger.emit(str('stop'))

    def run(self):
        self.init()
        print("【自动福利】邮件开始执行")
        while self.running:
            self._run()
            self.sleep(1)

    def stop(self):
        print("【自动福利】复活币福利执行结束")
        self.running = False
