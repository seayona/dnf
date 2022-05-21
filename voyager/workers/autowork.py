from configparser import ConfigParser

from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QEventLoop

from voyager.game import Game, Player
from voyager.infrastructure import Notification
from voyager.recognition import Recogbot
from voyager.workers import PlayerFightWorker, GameWorker, PlayerSkillCooldownWorker, PlayerAttackWorker


class AutoStriveWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)
    conf_path = './conf/auto.ini'

    def __init__(self):
        # 初始化函数，默认
        super(AutoStriveWorker, self).__init__()
        self.game = Game()
        self.recogbot = Recogbot()
        self.player = Player('Seayona')
        self.notification = Notification()

        self.working = False
        self.workers = []
        self.strivers = []
        self._init_conf()
        self._init_striver()
        self._init_worker()

    def _cooldown(self):
        self.player.cooldown()

    def _attack(self):
        self.player.attack()

    def _init_worker(self):
        # 战斗线程
        f = PlayerFightWorker(self.game, self.recogbot, self.player)
        f.trigger.connect(self._working_stop)
        self.workers.append(f)

        # 雪山场景检测
        g = GameWorker(self.game, self.recogbot)
        g.trigger.connect(self._working_stop)
        self.workers.append(g)

        a = PlayerAttackWorker(self.player)
        a.trigger.connect(self._working_stop)
        self.workers.append(a)

        c = PlayerSkillCooldownWorker(self.player)
        c.trigger.connect(self._working_stop)
        self.workers.append(c)

    def _init_conf(self):
        print("【探索者】读取角色配置")
        config = ConfigParser()
        config.read('conf/player.ini', encoding='UTF-8')
        players = config.sections()
        print("【探索者】读取到的角色", players)
        self.strivers = list(filter(lambda p: config.get(p, 'Work') == 'Strive', players))
        print("【探索者】读取到的砖工", self.strivers)
        # self.boys = list(filter(lambda p: config.get(p, 'Work') == 'LevelUp', self.players))
        # print("【探索者】读取到的小号", self.boys)

    def _init_striver(self):
        striver = self._current()
        if striver is None or striver not in self.strivers:
            striver = self.strivers[0]
        # 更新配置
        self._current_striver_update(striver)
        # 初始化角色
        self.player = Player(striver)

    def _current(self):
        conf = ConfigParser()
        conf.read(self.conf_path)
        player = conf.get('Strive', 'Player')
        return player

    def _current_striver_update(self, value):
        conf = ConfigParser()
        conf.read(self.conf_path)
        conf.set('Strive', 'Player', value)
        conf.write(open(self.conf_path, "w"))

    def _next_striver(self):
        current = self._current()
        if current in self.strivers:
            i = self.strivers.index(current)
            if i + 1 == len(self.strivers):
                print("【自动搬砖】所有角色搬砖完成")
                self._working_stop()
                self.trigger.emit('stop')
                return
            next_striver = self.strivers[i + 1]
        else:
            next_striver = self.strivers[0]
        return next_striver

    def _send(self, message):
        print(f"【自动搬砖】{message}")
        self.notification.send(message)

    def _working_stop(self):
        print("【自动搬砖】停止自动搬砖模式")
        for w in self.workers:
            w.stop()

        self.working = False

    def _fight(self):
        print(f"【自动搬砖】开启雪山战斗线程，当前角色{self.player}")
        for w in self.workers:
            w.start()
        # 标识开始战斗
        self.working = True

    def _working(self):
        print("【自动搬砖】5秒后前往雪山")
        self.game.snow_mountain_start(self._fight)

    def _run(self):
        # 如果角色疲劳值耗尽，并且在城镇中，切换角色
        if self.player.tired() and self.recogbot.town():
            # self.trigger.emit('stop')
            # 切换成功，设置当前角色
            def callback(player):
                # 更新配置
                self.player = Player(player)
                self._current_striver_update(player)
                self._send(f"【{player}】开始搬砖")

            next_player = self._next_striver()
            print(f"【自动搬砖】疲劳值耗尽，切换角色{next_player}")
            self._working_stop()
            self.game.switch(next_player, callback)

        # 疲劳值未耗尽，人在城镇中，去搬砖
        if self.recogbot.town() and not self.player.tired():
            print(f"【自动搬砖】疲劳值还有，人在城镇中，去搬砖")
            # 防止重复开启线程
            self._working()

        # 疲劳值未耗尽，人在地下城中，继续战斗
        if not self.working and (self.recogbot.result() or self.recogbot.jump()) and not self.player.tired():
            print(f"【自动搬砖】疲劳值还有，人在地下城中，继续战斗")
            # 防止重复开启线程
            self._fight()

        # 疲劳值不足，人在地下城中，返回城镇
        if self.player.tired() and (self.recogbot.jump() or self.recogbot.result()):
            print(f"【自动搬砖】疲劳值不足，返回城镇")
            self._working_stop()
            self.game.town()

        # 疲劳值不足，打完深渊图的时候，返回城镇
        if self.recogbot.insufficient_balance_demon():
            print(f"【自动搬砖】疲劳值不足，返回城镇")
            self._working_stop()
            self.player.over_fatigued()

        # 疲劳值不足，再次挑战的时候，返回城镇
        if self.recogbot.insufficient_balance():
            print(f"【自动搬砖】疲劳值不足，返回城镇")
            self._working_stop()
            self.player.over_fatigued()

    def run(self):
        print("【一键搬砖】一键搬砖开始执行")
        while True:
            self._run()

    def stop(self):
        print("【一键搬砖】一键搬砖停止执行")
        self._working_stop()
        self.terminate()
