from configparser import ConfigParser

from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QEventLoop

from voyager.game import Game, Player
from voyager.infrastructure import Notification
from voyager.recognition import Recogbot
from voyager.workers import PlayerFightWorker, GameWorker, PlayerSkillCooldownWorker, PlayerAttackWorker


class Auto(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)
    conf_path = './conf/auto.ini'

    def __init__(self, profession):
        # 初始化函数，默认
        super(Auto, self).__init__()
        self.game = Game()
        self.recogbot = Recogbot()
        self.player = Player('Aorist')
        self.notification = Notification()

        self.working = False
        self.profession = profession
        self.workers = []
        self.piglets = []
        self._init_conf()
        self._init_piglet()
        self._init_worker()

    def _cooldown(self):
        self.player.cooldown()

    def _attack(self):
        self.player.attack()

    def _set_player(self, player):
        self.player = Player(player)

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
        self.piglets = list(filter(lambda p: config.get(p, 'Work') == self.profession, players))

    def _init_piglet(self):
        piglet = self._current()
        if piglet is None or piglet not in self.piglets:
            piglet = self.piglets[0]
        # 更新配置
        self._current_piglet_update(piglet)
        # 初始化角色
        self.player = Player(piglet)

    def _current(self):
        conf = ConfigParser()
        conf.read(self.conf_path)
        player = conf.get(self.profession, 'Player')
        return player

    def _current_piglet_update(self, value):
        conf = ConfigParser()
        conf.read(self.conf_path)
        conf.set(self.profession, 'Player', value)
        conf.write(open(self.conf_path, "w"))

    def _next_piglet(self):
        current = self._current()
        if current in self.piglets:
            i = self.piglets.index(current)
            if i + 1 == len(self.piglets):
                print("【Auto Work】所有角色工作完成")
                self._working_stop()
                self.trigger.emit('stop')
                return
            next_piglet = self.piglets[i + 1]
        else:
            next_piglet = self.piglets[0]
        return next_piglet

    def _send(self, message):
        print(f"【Auto Work】{self.profession} {message}")
        self.notification.send(message)

    def _working_stop(self):
        print("【Auto Work】停止自动模式")
        for w in self.workers:
            w.stop()
        self.working = False
        self.player.over_fatigued()

    def _switch_player(self):
        print('我进来了')
        next_player = self._next_piglet()
        self.game.switch(next_player, lambda player: (
            self._set_player(player), self._current_striver_update(player), self._send(f"【{player}】开始搬砖")))

    def _fight(self):
        print(f"【Auto Work】开启战斗线程，当前角色{self.player}")
        for w in self.workers:
            w.start()
        # 标识开始战斗
        self.working = True

    def _run(self):
        pass

    def run(self):
        print("【Auto Work】Auto Work开始执行")
        while True:
            self._run()

    def stop(self):
        print("【Auto Work】Auto Work停止执行")
        self._working_stop()
        self.terminate()
