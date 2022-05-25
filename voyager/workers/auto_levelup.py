from .auto import Auto
from .agency_mission import AgencyMissionWorker
from .player_mission_fight import PlayerMissionFightWorker
from .player_attack import PlayerAttackWorker
from .player_cooldown import PlayerSkillCooldownWorker


class AutoLevelUpWorker(Auto):
    def __init__(self, new_valley):
        super(AutoLevelUpWorker, self).__init__('LevelUp', new_valley)

    def _init_worker(self):
        super(AutoLevelUpWorker, self)._init_worker()
        # 升级任务检测
        self.workers['main'] = {}
        self.workers['main']['thread'] = []
        m = AgencyMissionWorker(self.game, self.recogbot, self.player)
        m.trigger.connect(self._working_stop)
        self.workers['main']['thread'].append(m)

        f = PlayerMissionFightWorker(self.game, self.recogbot, self.player)
        f.trigger.connect(self._working_stop)
        self.workers['main']['thread'].append(f)

        s = PlayerSkillCooldownWorker(self.player)
        self.workers['main']['thread'].append(s)

        a = PlayerAttackWorker(self.player)
        self.workers['main']['thread'].append(a)
        self.workers['main']['working'] = 0

    def _run(self):
        super(AutoLevelUpWorker, self)._run()
