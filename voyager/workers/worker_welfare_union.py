import time

from PyQt5.QtCore import QThread, pyqtSignal


class WelfareUnionWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareUnionWorker, self).__init__()
        self.game = voyager.game
        self.recogbot = voyager.recogbot
        self.player = voyager.player

    def _run(self):
        # 在城镇中，还没有签到
        if self.recogbot.town():
            self.game.union_sign_start()

        # 发现签到按钮
        if self.recogbot.union_sign():
            self.game.union_sign()

        # 发现宝箱1
        if self.recogbot.union_sign_box1():
            self.game.union_sign_box1()

        # 发现宝箱2
        if self.recogbot.union_sign_box2():
            self.game.union_sign_box2()

        # 发现宝箱3
        if self.recogbot.union_sign_box3():
            self.game.union_sign_box3()

        # 发现宝箱4
        if self.recogbot.union_sign_box4():
            self.game.union_sign_box4()

        # 宝箱1、2、3都领了并且金币签到过了
        if self.recogbot.union_signed():
            print("【公会福利】工会福利领取完成")
            self.game.union_signed(lambda: (self.player.over_welfare(), self.trigger.emit(str('stop'))))

    def run(self):
        print("【公会福利】公会福利开始执行", int(QThread.currentThreadId()))
        while True:
            self._run()

    def stop(self):
        print("【公会福利】公会福利开始执行")
        self.terminate()
