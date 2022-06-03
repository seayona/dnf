import time

from PyQt5.QtCore import QThread, pyqtSignal


class WelfareRevivalCoinWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareRevivalCoinWorker, self).__init__()
        self.voyager = voyager
        self.running = False

    def init(self):
        self.running = True

    def _run(self):

        # 没领取打开商城页面
        if self.voyager.recogbot.town() and not self.voyager.player.welfare['revival_coin']:
            self.voyager.game.goto_mall_recovered_product()

        # 已领取
        if self.voyager.recogbot.revival_coin_received():
            self.voyager.player.welfare['revival_coin'] = True
            self.voyager.game.back_town_coin_received()

        # 可以领取
        if self.voyager.recogbot.revival_coin_status():
            self.voyager.game.mall_purchase()

        # 领取后在城镇stop
        if self.voyager.recogbot.town() and self.voyager.player.welfare['revival_coin']:
            self.trigger.emit(str('stop'))

    def run(self):
        self.init()
        print("【自动福利】复活币福利开始执行")
        while self.running:
            self._run()
            self.sleep(1)

    def stop(self):
        print("【自动福利】复活币福利执行结束")
        self.running = False
