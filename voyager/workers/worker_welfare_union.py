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
        self.boxs = []
        self._init_box()

    def _init_box(self):
        self.boxs = []
        for i in range(5):
            self.boxs.append({'signed': False, 'target': "union_box{}_helper".format(i + 1)})

    def _box_signed_true(self, box):
        box['signed'] = True

    def _run(self):
        # 在城镇中，还没有签到
        if self.recogbot.town():
            self.game.union_sign_start()

        # 发现签到按钮
        if self.recogbot.union_sign():
            self.game.union_sign()

        not_signed_box = list(filter(lambda item: not item['signed'], self.boxs))
        if len(not_signed_box):
            box = not_signed_box[0]
            self.game.union_box_sign(box['target'], lambda: self._box_signed_true(box))

        if not self.recogbot.union_sign() and len(not_signed_box) == 0:
            print("【公会福利】工会福利领取完成")
            self.game.union_signed(lambda: (self.player.over_welfare(), self.trigger.emit(str('stop'))))


    def run(self):
        print("【公会福利】公会福利开始执行", int(QThread.currentThreadId()))
        self._init_box()
        while True:
            self._run()

    def stop(self):
        print("【公会福利】公会福利开始执行")
        self.terminate()
