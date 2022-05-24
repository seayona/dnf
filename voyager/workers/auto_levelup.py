from voyager.workers.auto import Auto
from voyager.game import Player
from voyager.workers import AgencyMissionWorker, PlayerMissionFightWorker, PlayerSkillCooldownWorker, PlayerAttackWorker


class AutoLevelUp(Auto):
    def __init__(self):
        super(AutoLevelUp, self).__init__('LevelUp')

    def _init_worker(self):
        # 升级任务检测
        m = AgencyMissionWorker(self.game, self.recogbot, self.player)
        m.trigger.connect(self._working_stop)
        self.workers.append(m)

        f = PlayerMissionFightWorker(self.game, self.recogbot, self.player)
        f.trigger.connect(self._working_stop)
        self.workers.append(f)

        s = PlayerSkillCooldownWorker(self.player)
        self.workers.append(s)

        a = PlayerAttackWorker(self.player)
        self.workers.append(a)

    def _run(self):
        if self.player.tired() and self.recogbot.town():
            self._switch_player()

        if not self.working and not self.player.tired():
            self._fight()
