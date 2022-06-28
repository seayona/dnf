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
        self.init_chance = -1

    def init(self):
        self.running = True
        self.init_chance = -1
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
                {'signed': False, 'target': f'duel_day_box{i}', 'uncompleted': f'duel_day_box{i}_uncompleted',
                 'signed_target': f'duel_day_box{i}_signed'})

        for i in range(1, 6):
            self.reward['week']['box'].append(
                {'signed': False, 'target': f'duel_week_box{i}', 'uncompleted': f'duel_week_box{i}_uncompleted',
                 'signed_target': f'duel_week_box{i}_signed'})

    def _box_signed(self, box):
        box['signed'] = True

    def _run(self):
        # 进入角斗场
        if self.voyager.recogbot.town() and not self.voyager.player.winner():
            self.voyager.game.goto_duel()

        if self.voyager.recogbot.duel_ai_fight() and not self.voyager.player.winner():
            self.voyager.game.duel_ai_fight()

        # 赛季结束结算
        if self.voyager.recogbot.duel_season_over():
            self.voyager.game.duel_season_over()

        if self.voyager.recogbot.duel_promotion():
            self.voyager.game.duel_promotion()

        # 从技能界面返回
        if self.voyager.recogbot.skill_back():
            self.voyager.game.skill_back()

        # 设置技能
        if self.voyager.recogbot.duel_skill_title():
            self.voyager.game.duel_skill_set()

        if self.voyager.recogbot.confirm():
            self.voyager.game.confirm()
        # self.voyager.player.over_duel('fight')
        if self.init_chance == -1:
            self.init_chance = self._recog_chance()
            return

        if not self.voyager.player.duel_status('fight'):
            current = self._recog_chance()
            if not current == -1:
                # 挑战
                if self.voyager.recogbot.duel_chance(0) or self.init_chance - current >= 3:
                    self.voyager.player.over_duel('fight')
                else:
                    self.voyager.matric.heartbeat()
                    self.voyager.game.duel_challenge()

        # 领取奖励
        if self.voyager.player.duel_status('fight') and not self.voyager.player.duel_status('reward'):
            if self.voyager.recogbot.duel_reward():
                self.voyager.game.duel_reward()
            # 每日领取
            if self.voyager.recogbot.duel_day_active():
                self._get_reward('day')

            # 领取完毕，切换每周
            if self.voyager.recogbot.duel_day_active() and self.reward['day']['signed']:
                self.voyager.game.duel_week()

            # 每周领取
            if self.voyager.recogbot.duel_week_active():
                self._get_reward('week')

            # 全部领取完毕
            if self.reward['day']['signed'] and self.reward['week']['signed']:
                self.voyager.player.over_duel('reward')
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
                    if self.voyager.recogbot.recog_any(item['signed_target']) or self.voyager.recogbot.recog_any(
                            item['uncompleted']):
                        item['signed'] = True

                not_signed = list(filter(lambda i: not i['signed'], self.reward[type]['box']))
                if len(not_signed) > 0:
                    self.voyager.game.duel_box_sign(not_signed[0], lambda: self._box_signed(not_signed[0]))

                if len(not_signed) == 0 and self.reward[type]['get_all']:
                    self.reward[type]['signed'] = True

    def _recog_chance(self):
        for i in range(7):
            if self.voyager.recogbot.duel_chance(i):
                return i
        return -1

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
