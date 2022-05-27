from .auto import Auto
from .agency_mission import AgencyMissionWorker
from .player_mission_fight import PlayerMissionFightWorker
from .player_attack import PlayerAttackWorker
from .player_cooldown import PlayerSkillCooldownWorker


class AutoLevelUpWorker(Auto):
    def __init__(self, new_valley, new_welfare):
        super(AutoLevelUpWorker, self).__init__('LevelUp', new_valley, new_welfare)

    def _init_worker(self):
        super(AutoLevelUpWorker, self)._init_worker()
        # 升级任务检测
        m = AgencyMissionWorker(self.game, self.recogbot, self.player)
        m.trigger.connect(self._working_stop)

        f = PlayerMissionFightWorker(self.game, self.recogbot, self.player)
        f.trigger.connect(self._working_stop)

        s = PlayerSkillCooldownWorker(self.player)

        a = PlayerAttackWorker(self.player)

        # 装配到works
        self._worker_assembly(work_name='main', thread=[m, f, s, a], init_working=0)

    def _run(self):
        super(AutoLevelUpWorker, self)._run()
