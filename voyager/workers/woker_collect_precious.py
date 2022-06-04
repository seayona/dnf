import time

from PyQt5.QtCore import QThread, pyqtSignal


class CollectPrecious(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareMailReceive, self).__init__()
        self.voyager = voyager
        self.running = False
        self.preciouses = []
        self.detect_count = 0

    def init(self):
        self.running = True
        self.detect_count = 0
        self.preciouses = [
            {

                'list': [
                    {'name': '碳', 'target': '', 'collect': False},
                    {'name': '深渊票', 'target': '', 'collect': False},
                    {'name': '红宝石', 'target': '', 'collect': False},
                    {'name': '蓝宝石', 'target': '', 'collect': False},
                    {'name': '绿宝石', 'target': '', 'collect': False},
                    {'name': '紫宝石', 'target': '', 'collect': False},
                    {'name': '钻石', 'target': '', 'collect': False},
                    {'name': '布片', 'target': '', 'collect': False},
                    {'name': '碎骨', 'target': '', 'collect': False},
                    {'name': '砥石', 'target': '', 'collect': False},
                    {'name': '布片', 'target': '', 'collect': False},
                    {'name': '皮革', 'target': '', 'collect': False},
                    {'name': '白眼', 'target': '', 'collect': False},
                    {'name': '蓝眼', 'target': '', 'collect': False},
                    {'name': '紫眼', 'target': '', 'collect': False},
                    {'name': '粉眼', 'target': '', 'collect': False},
                    {'name': '金眼', 'target': '', 'collect': False},
                ],
                'target': '',
                'target_active': '',
                'clear': False
            },
            {
                'list': [{'name': '雪山卡', 'target': '', 'collect': False}],
                'target': '',
                'target_active': '',
                'clear': False
            }
        ]

    def detect_add(self):
        self.detect_count += 1

    def _run(self):
        cls = self.voyager.recogbot.detect()
        # 入库完毕，在城镇
        if self.voyager.recogbot.town() and self.voyager.player.collected:
            self.trigger.emit(str('stop'))
            return

        # 还没入库，在城镇去金库
        if self.voyager.recogbot.town() and not self.voyager.player.collected and cls['bag'][0]:
            self.voyager.game.goto_vault(cls['bag'])
            return

        # 入库完毕，不在城镇中，返回城镇
        if not self.voyager.recogbot.town() and not self.voyager.player.collected:
            self.voyager.game.back_town_vault()
            return

        not_collect = list(filter(lambda key: not self.preciouses[key]['clear'], self.preciouses))

        # 账号金库激活，材料未收集
        if self.voyager.recogbot.gang_vault_active() and len(not_collect) > 0:
            not_collect_preciouses = list(filter(lambda k: not k['collect'], not_collect[0]['list']))

            # [入库操作过3次，有空格子] or [入库所有标记True] or [入库操作过5次] ->本项入库完成
            if (self.detect_count > 3 and self.voyager.recogbot.recog_empty_cell()) or len(
                    not_collect_preciouses) == 0 or self.detect_count > 5:
                not_collect[0]['clear'] = True
                return

                # 不在界面，导航过去
            if self.voyager.recogbot.recog_any(not_collect[0]['target']):
                self.voyager.game.click_any(not_collect[0]['target'])

            # 在界面，开始处理
            if self.voyager.recogbot.recog_any(not_collect[0]['target_active']):
                self.voyager.game.precious_to_vault(not_collect_preciouses, lambda: self.detect_add())

        if len(not_collect) == 0:
            self.voyager.player.over_collect()

    def run(self):
        self.init()
        print("【自动入包】开始执行")
        while self.running:
            self._run()
            self.sleep(1)

    def stop(self):
        print("【自动入包】利执行结束")
        self.running = False
