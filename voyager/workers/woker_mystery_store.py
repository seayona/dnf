import time

from PyQt5.QtCore import QThread, pyqtSignal


class MysteryStore(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(MysteryStore, self).__init__()
        self.voyager = voyager
        self.running = False
        self.commodity = []
        self.current = None

    def init(self):
        self.running = True
        self.current = None
        self.commodity = [
            {"name": "钥匙碎片", "target": "/store/key_fragment", "complete": False},
            {"name": "钥匙", "target": "/store/key", "complete": False},
            {"name": "调整箱碎片", "target": "/store/transform_fragment", "complete": False},
            {"name": "调整箱", "target": "/store/transform", "complete": False},
            {"name": "HP", "target": "/store/hp", "complete": False},
            {"name": "徽章箱", "target": "/store/badge", "complete": False},
            {"name": "材料箱", "target": "/store/material", "complete": False},
            {"name": "宝石箱", "target": "/store/stone", "complete": False},
            {"name": "碳", "target": "/store/carbon", "complete": False},
            {"name": "雷米", "target": "/store/remy", "complete": False},
            {"name": "复活币", "target": "/store/coin", "complete": False}
        ]

    def _run(self):
        if self.voyager.recogbot.town() and not self.voyager.player.mystery_store:
            self.voyager.game.goto_ms()

        # 任务完成，一路esc
        if self.voyager.player.mystery_store and not self.voyager.recogbot.town():
            self.voyager.game.esc()

        if self.voyager.player.mystery_store and self.voyager.recogbot.town():
            self.voyager.matric.heartbeat()
            self.trigger.emit(self.__class__.__name__)

        # 确认按钮
        if self.voyager.recogbot.confirm():
            self.voyager.matric.heartbeat()
            self.voyager.game.confirm()
            self.voyager.player.over_shopping()

        not_complete = list(filter(lambda item: not item['complete'], self.commodity))

        # 无可购买物品
        if len(not_complete) == 0 and not self.voyager.recogbot.purchase():
            self.voyager.player.over_shopping()

        if len(not_complete) == 0 and self.voyager.recogbot.purchase():
            self.voyager.game.purchase()

        if self.voyager.recogbot.in_mystery_store() and self.current is None and len(not_complete) > 0:
            result = self.voyager.recogbot.detect_commodity(not_complete[0]['target'])
            if result is None:
                not_complete[0]['complete'] = True
                return
            self.current = not_complete[0]
            self.voyager.game.ms_check_commodity(result, lambda: self._over_current())

    def _over_current(self):
        self.current['complete'] = True
        self.current = None

    def run(self):
        self.init()
        print("【神秘商店】开始执行")
        while self.running:
            self._run()
            self.sleep(1)

    def stop(self):
        print("【神秘商店】执行结束")
        self.running = False
