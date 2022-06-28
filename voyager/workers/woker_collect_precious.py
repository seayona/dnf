import time

from PyQt5.QtCore import QThread, pyqtSignal


class CollectPrecious(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(CollectPrecious, self).__init__()
        self.voyager = voyager
        self.running = False
        self.preciouses = []
        self.detect_count = 0
        self.busy = False

    def init(self):
        self.running = True
        self.detect_count = 0
        self.preciouses = [
            {
                'list': [
                    {'name': '碳', 'target': 'carbon', 'collect': 0},
                    {'name': '深渊票', 'target': 'abyss', 'target_binding': 'abyss_bind', 'collect': 0},
                    {'name': '洗练石', 'target': 'stone_wash', 'collect': 0},
                    {'name': '红宝石', 'target': 'stone_red', 'collect': 0},
                    {'name': '蓝宝石', 'target': 'stone_blue', 'collect': 0},
                    {'name': '绿宝石', 'target': 'stone_green', 'collect': 0},
                    {'name': '紫宝石', 'target': 'stone_purple', 'collect': 0},
                    {'name': '钻石', 'target': 'crystal', 'target_binding': 'crystal_bind', 'collect': 0},
                    {'name': '布片', 'target': 'cloth', 'collect': 0},
                    {'name': '碎骨', 'target': 'bone', 'collect': 0},
                    {'name': '砥石', 'target': 'whetstone', 'collect': 0},
                    {'name': '铁片', 'target': 'iron', 'collect': 0},
                    {'name': '皮革', 'target': 'leather', 'collect': 0},
                    {'name': '白眼', 'target': 'eye_white', 'collect': 0},
                    {'name': '蓝眼', 'target': 'eye_blue', 'collect': 0},
                    {'name': '紫眼', 'target': 'eye_purple', 'collect': 0},
                    {'name': '粉眼', 'target': 'eye_pink', 'collect': 0},
                    {'name': '金眼', 'target': 'eye_gold', 'collect': 0},
                    {'name': '印章1', 'target': 'seal1', 'target_binding': 'seal1_bind', 'collect': 0},
                    {'name': '印章2', 'target': 'seal2', 'target_binding': 'seal2_bind', 'collect': 0},
                    {'name': '结晶', 'target': 'crystallization', 'target_binding': 'crystallization_bind', 'collect': 0},
                ],
                'target': 'material',
                'target_active': 'material_active',
                'clear': False
            },
            {
                'list': [{'name': '雪山卡', 'target': 'snow_mountain_card', 'collect': 0}],
                'target': 'card',
                'target_active': 'card_active',
                'clear': False
            }
        ]

    def detect_add(self):
        self.detect_count += 1
        self.busy = False

    def _run(self):
        cls = self.voyager.recogbot.detect()
        # 入库完毕，在城镇
        if self.voyager.recogbot.town() and self.voyager.player.collected:
            self.trigger.emit(self.__class__.__name__)
            return

        # 还没入库，在城镇去金库
        if self.voyager.recogbot.town() and not self.voyager.player.collected and cls['bag'][0]:
            self.voyager.matric.heartbeat()
            self.voyager.game.goto_vault(cls['bag'])
            return

        # 入库完毕，不在城镇中，返回城镇
        if not self.voyager.recogbot.town() and self.voyager.player.collected:
            self.voyager.game.back_town_vault()
            return
        not_collect = list(filter(lambda v: not v['clear'], self.preciouses))

        # 账号金库激活，材料未收集
        if self.voyager.recogbot.gang_vault_active() and len(not_collect) > 0:
            not_collect_preciouses = list(filter(lambda k: not k['collect'] == 2, not_collect[0]['list']))
            # [入库操作过3次，有空格子] or [入库所有标记True] or [入库操作过5次] ->本项入库完成
            if ((self.detect_count > 2 and self.voyager.recogbot.has_empty_cell()) or len(
                    not_collect_preciouses) == 0 or self.detect_count > 5) and not self.busy:
                not_collect[0]['clear'] = True
                self.detect_count = 0
                return

            # 不在界面，导航过去
            if self.voyager.recogbot.recog_any(not_collect[0]['target']):
                self.voyager.game.click_any(not_collect[0]['target'])

            # 在界面，开始处理
            if self.voyager.recogbot.recog_any(not_collect[0]['target_active']) and not self.busy:
                self.busy = True
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
