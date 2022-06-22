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
                'box': []
            }
        }
        for i in range(1, 4):
            self.reward['day']['box'].append(
                {'signed': False, 'target': f'duel_day_box{i}', 'signed_target': f'duel_day_box{i}_signed'})

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
            if self.voyager.recogbot.duel_everyday():
                # 一键领取
                if self.voyager.recogbot.duel_get_all():
                    self.voyager.game.duel_get_all()
                    self.reward['every']['get_all'] = True

                not_signed = list(filter(lambda i: not i['signed'], self.reward['day']['box']))



        if self.voyager.recogbot.town() and self.voyager.player.winner():
            self.trigger.emit(self.__class__.__name__)

    def run(self):
        self.init()
        print(f"【{self.current_work}】{self.current_work}开始执行")
        while self.running:
            self._run()
            time.sleep(0.5)

    def stop(self):
        print(f"【{self.current_work}】{self.current_work}停止执行")
        for s in self.workers:
            s.stop()
        self.running = False
