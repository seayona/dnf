import time

from PyQt5.QtCore import QThread, pyqtSignal


class WelfareUnionWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareUnionWorker, self).__init__()
        self.voyager = voyager
        self.boxs = []
        self._init_box()
        self.running = False

    def init(self):
        self.running = True

    def _init_box(self):
        self.boxs = []
        for i in range(5):
            self.boxs.append({'signed': False, 'target': "union_box{}_helper".format(i + 1),
                              'target_kr': "union_box{}_helper_kr".format(i + 1)})

    def _box_signed_true(self, box):
        box['signed'] = True

    def _run(self):
        # 在城镇中，还没有签到
        if self.voyager.recogbot.town() and not self.voyager.player.welfare['union']:
            self.voyager.game.union_sign_start()

        # 在城镇中，已签到
        if self.voyager.player.welfare['union'] and self.voyager.recogbot.town():
            self.trigger.emit(self.__class__.__name__)

        # 发现签到按钮
        if (not self.voyager.recogbot.town()) and self.voyager.recogbot.union_sign() and not \
        self.voyager.player.welfare['union']:
            self.voyager.game.union_sign()

        for index in range(len(self.boxs)):
            if self.voyager.recogbot.union_box_signed(index):
                self._box_signed_true(self.boxs[index])

        not_signed_box = list(filter(lambda item: not item['signed'], self.boxs))
        if (not self.voyager.recogbot.town()) and len(not_signed_box) != 0:
            box = not_signed_box[0]
            self.voyager.game.union_box_sign(box['target'], box['target_kr'], lambda: self._box_signed_true(box))

        if (not self.voyager.recogbot.town()) and len(not_signed_box) == 0:
            print("【公会福利】工会福利领取完成")
            self.voyager.player.over_welfare('union')
            self.voyager.game.back_town_union_signed()

        if self.voyager.recogbot.get_one():
            self.voyager.game.esc()

    def run(self):
        self.init()
        self._init_box()
        print("【公会福利】公会福利开始执行", int(QThread.currentThreadId()))
        while self.running:
            self._run()

    def stop(self):
        print("【公会福利】公会福利开始执行")
        self.running = False
