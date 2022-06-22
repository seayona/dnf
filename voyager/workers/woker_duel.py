import time

from PyQt5.QtCore import QThread, pyqtSignal

from .player_fight_snowmountain import PlayerFightWorker
from .player_fight_attack import PlayerAttackWorker
from .player_fight_cooldown import PlayerSkillCooldownWorker


class DuelWork(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        # 初始化函数，默认
        super(DuelWork, self).__init__()
        self.voyager = voyager
        self.running = False
        self.workers = []
        self.reward = {}

    def init(self):
        self.reward = {
            'day': {
                'get_all': False,
                'box': [],
                'signed': False
            },
            'week': {
                'get_all': False,
                'box': [],
                'signed': False
            }
        }
        for i in range(1, 4):
            self.reward['day']['box'].append(
                {'signed': False, 'target': f'duel_day_box{i}', 'signed_target': f'duel_day_box{i}_signed'})

        for i in range(1, 6):
            self.reward['day']['box'].append(
                {'signed': False, 'target': f'duel_week_box{i}', 'signed_target': f'duel_week_box{i}_signed'})

    def _box_signed(self, box):
        box['signed'] = True

    def _run(self):
        # 进入角斗场
        if self.voyager.recogbot.town() and not self.voyager.player.winner():
            self.voyager.game.goto_duel()

        # 挑战
        if self.voyager.recogbot.duel_chance(0):
            self.voyager.player.over_duel('fight')
        else:
            self.voyager.game.duel_challenge()

        if self.voyager.recogbot.confirm():
            self.voyager.game.confirm()

        # 领取奖励
        if self.voyager.player.duel_status('fight') and not self.voyager.player.duel_status('reward'):
            if self.voyager.recogbot.duel_reward():
                self.voyager.game.duel_reward()

        # 每日领取
        if self.voyager.recogbot.duel_day_active():
            self._get_reward('day')

        # 领取完毕，切换每周
        if self.voyager.recogbot.duel_day_active() and self.reward[type]['signed']:
            self.voyager.game.duel_week()

        # 每周领取
        if self.voyager.recogbot.duel_week_active():
            self._get_reward('week')

        # 全部领取完毕
        if self.reward['day']['signed'] and self.reward['week']['signed']:
            self.voyager.player.over_duel()

        # 一路按esc返回
        if self.voyager.player.winner() and not self.voyager.recogbot.town():
            self.voyager.game.esc()

        if self.voyager.recogbot.town() and self.voyager.player.winner():
            self.trigger.emit(self.__class__.__name__)

    # 奖励领取
    def _get_reward(self, type):
        if not self.reward[type]['signed']:
            # 一键领取
            if self.voyager.recogbot.duel_get_all():
                self.voyager.game.duel_get_all()
                self.reward[type]['get_all'] = True

            if self.voyager.recogbot.duel_get_all_grey():
                self.reward[type]['get_all'] = True
                # 领取箱子
                not_signed = list(filter(lambda i: not i['signed'], self.reward[type]['box']))
                for item in not_signed:
                    if self.voyager.recogbot.recog_any(item['signed_target']):
                        item['signed'] = True

                not_signed = list(filter(lambda i: not i['signed'], self.reward[type]['box']))
                if len(not_signed) > 0:
                    self.voyager.game.duel_box_sign(not_signed[0], lambda: self._box_signed(not_signed[0]))

                if len(not_signed) == 0 and self.reward[type]['get_all']:
                    self.reward[type]['signed'] = True

    def run(self):
        self.init()
        print(f"【角斗场】开始执行")
        while self.running:
            self._run()
            time.sleep(0.5)

    def stop(self):
        print(f"【角斗场】停止执行")
        for s in self.workers:
            s.stop()
        self.running = False
