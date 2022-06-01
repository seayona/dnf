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
        cls = self.voyager.recogbot.detect()

        # 在城镇中，还没有签到
        if cls['menu'][0] and not self.voyager.player.welfare['union']:
            self.voyager.game.union_sign_start()

        # 发现签到按钮
        if self.voyager.recogbot.union_sign() and not self.voyager.player.welfare['union']:
            self.voyager.game.union_sign()

        for index in range(len(self.boxs)):
            if self.voyager.recogbot.union_box_signed(index):
                self._box_signed_true(self.boxs[index])

        not_signed_box = list(filter(lambda item: not item['signed'], self.boxs))
        if len(not_signed_box) and not self.voyager.player.welfare['union']:
            box = not_signed_box[0]
            self.voyager.game.union_box_sign(box['target'], box['target_kr'], lambda: self._box_signed_true(box))

        if not self.voyager.recogbot.union_sign() and len(not_signed_box) == 0 and not self.voyager.player.welfare['union']:
            print("【公会福利】工会福利领取完成")
            self.voyager.player.over_welfare('union')
            self.voyager.game.back_town_union_signed()

        if self.voyager.player.welfare['union'] and cls['menu'][0]:
            self.trigger.emit(str('stop'))

    def run(self):
        self.init()
        self._init_box()
        print("【公会福利】公会福利开始执行", int(QThread.currentThreadId()))
        while self.running:
            self._run()

    def stop(self):
        print("【公会福利】公会福利开始执行")
        self.running = False
