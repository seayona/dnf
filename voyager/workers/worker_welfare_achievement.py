import time

from PyQt5.QtCore import QThread, pyqtSignal


class WelfareAchievementWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareAchievementWorker, self).__init__()
        self.voyager = voyager
        self.running = False
        self.daily = False
        self.weekly = False

    def init(self):
        self.running = True
        self.daily = False
        self.weekly = False

    def _run(self):
        cls = self.voyager.recogbot.detect()

        # 没领取打开成就页面
        if cls['menu'][0] and not self.voyager.player.welfare['achievement']:
            self.voyager.game.goto_achievement()

        # 在每日页面
        if self.voyager.recogbot.achievement_daily_active():
            # 有还没领取的，进行领取
            if self.voyager.recogbot.achievement_daily_box():
                self.voyager.game.achievement_daily_box()
                return
            if self.voyager.recogbot.get_all():
                self.voyager.game.achievement_get_all()
                return
            if self.voyager.recogbot.achievement_daily_sella():
                self.voyager.game.achievement_daily_sella()
                return
            self.daily = True

        # 每日领取完，去每周
        if self.daily and self.voyager.recogbot.achievement_in_daily():
            self.voyager.game.goto_achievement_weekly()

        if self.voyager.recogbot.achievement_weekly_active():
            # 每周奖励领取
            if self.voyager.recogbot.get_all():
                self.voyager.game.achievement_get_all()
                return
            if self.voyager.recogbot.weekly_box():
                self.voyager.game.achievement_weekly_box()
                return
            self.weekly = True

        if self.weekly and self.daily:
            self.voyager.player.welfare['achievement'] = True
            self.voyager.game.back_town_achievement()

        # 领取后在城镇stop
        if cls['menu'][0] and self.voyager.player.welfare['achievement']:
            self.trigger.emit(str('stop'))

    def run(self):
        self.init()
        print("【每日福利】每日福利开始执行", int(QThread.currentThreadId()))
        while self.running:
            self._run()

    def stop(self):
        print("【每日福利】每日福利停止执行")
        self.running = False
