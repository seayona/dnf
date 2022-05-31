import time

from PyQt5.QtCore import QThread, pyqtSignal


class WelfareAchievementWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareAchievementWorker, self).__init__()
        self.voyager = voyager
        self.running = False
        self.daily = {'one_key': False, box: False}
        self.weekly = {'one_key': False, box: False}

    def init(self):
        self.running = True

    def _run(self):
        # 领取后还在每日返回
        if not self.voyager.recogbot.town() and self.voyager.player.welfare['daily']:
            self.voyager.game.esc()
            return

        # 领取后在城镇stop
        if self.voyager.recogbot.town() and self.voyager.player.welfare['daily']:
            self.trigger.emit(str('stop'))
            return

        # 没领取打开每日页面
        if self.voyager.recogbot.town() and not self.voyager.player.welfare['daily']:
            self.voyager.game.goto_mall_recovered_product()
            return



        if True:
            self.trigger.emit(str('stop'))

    def run(self):
        self.init()
        print("【每日福利】每日福利开始执行", int(QThread.currentThreadId()))
        while self.running:
            self._run()

    def stop(self):
        print("【每日福利】每日福利停止执行")
        self.running = False
