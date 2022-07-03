import time

from PyQt5.QtCore import QThread, pyqtSignal


class UseConsumable(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(UseConsumable, self).__init__()
        self.voyager = voyager
        self.running = False
        self.consumable = []
        self.detect_count = 0
        self.current = {}
        self.in_consumable = False
        self.busy = False

    def init(self):
        self.running = True
        self.in_consumable = False
        self.busy = False
        self.current = {}
        self.detect_count = 0
        self.consumable = [{'name': '徽章', 'target': 'preciouses/badge', 'use': False},
                           {'name': '催化剂', 'target': 'preciouses/catalyzer', 'use': False},
                           {'name': '狗眼', 'target': 'preciouses/eye', 'use': False},
                           {'name': '狗眼2', 'target': 'preciouses/eye2', 'use': False},
                           {'name': '钥匙', 'target': 'preciouses/key', 'use': False},
                           {'name': '防具材料', 'target': 'preciouses/material', 'use': False},
                           {'name': '宝石材料', 'target': 'preciouses/stone', 'use': False},
                           {'name': '药水', 'target': 'preciouses/pill', 'use': False},
                           {'name': '公会箱子1', 'target': 'preciouses/union_box1', 'use': False},
                           {'name': '公会箱子2', 'target': 'preciouses/union_box2', 'use': False},
                           {'name': '公会箱子3', 'target': 'preciouses/union_box3', 'use': False},
                           {'name': '公会箱子4', 'target': 'preciouses/union_box4', 'use': False},
                           {'name': '公会箱子5', 'target': 'preciouses/union_box5', 'use': False}]

    def detect_add(self):
        self.detect_count += 1

    def _run(self):
        cls = self.voyager.recogbot.detect()
        # 入库完毕，在城镇
        if self.voyager.recogbot.town() and self.voyager.player.consumable:
            self.voyager.player.new_game()
            self.voyager.matric.heartbeat()
            self.trigger.emit(self.__class__.__name__)
            return

        # 还没使用
        if self.voyager.recogbot.town() and not self.voyager.player.consumable and cls['bag'][
            0] and not self.voyager.player.repair:
            self.voyager.game.repair_and_sale(cls['bag'], auto_back=False,
                                              callback=lambda: self.voyager.player.repaired())
            return

        # 使用完毕
        if not self.voyager.recogbot.town() and self.voyager.player.consumable and self.voyager.player.repair:
            self.voyager.game.back_town_vault()
            return

        if not self.voyager.recogbot.consumable_active() and self.voyager.player.repair and not self.in_consumable:
            self.voyager.game.goto_consumable()

        not_use = list(filter(lambda item: not item['use'], self.consumable))

        if self.voyager.recogbot.confirm() and self.voyager.player.repair:
            self.voyager.game.confirm()
            self._over_current()
            return

        if self.voyager.recogbot.csb_onekey():
            self.busy = True
            self.voyager.game.csb_onekey()
            return

        if self.voyager.recogbot.csb_use_large():
            self.busy = True
            self.voyager.game.csb_use_large()
            return

        if self.voyager.recogbot.csb_use() and not self.voyager.recogbot.csb_onekey():
            self.voyager.game.csb_use()
            self.busy = True
            return

        if self.voyager.recogbot.consumable_active():
            self.in_consumable = True
            if len(not_use) == 0 or self.detect_count >= 3:
                self.voyager.player.over_consumable()
                return
            if not self.busy:
                self._detect_csb(not_use)

    def _detect_csb(self, not_use):
        for c in not_use:
            if self.voyager.recogbot.recog_any(c['target']) and not self.busy:
                self.current = c
                self.detect_count = 0
                self.voyager.game.click_any(c['target'])
                return
        self.detect_add()

    def _over_current(self):
        self.current['use'] = True
        self.detect_count = 0
        self.busy = False

    def run(self):
        self.init()
        print("【自动使用消耗品】开始执行")
        while self.running:
            self._run()

    def stop(self):
        print("【自动使用消耗品】利执行结束")
        self.running = False
