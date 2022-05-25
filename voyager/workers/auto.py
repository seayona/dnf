from configparser import ConfigParser

from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QEventLoop

from voyager.game import Game, Player
from voyager.infrastructure import Notification
from voyager.recognition import Recogbot

from .game import GameWorker
from .player_fight import PlayerFightWorker
from .player_attack import PlayerAttackWorker
from .player_cooldown import PlayerSkillCooldownWorker
from .valley import ValleyWorker


class Auto(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)
    conf_path = './conf/auto.ini'

    def __init__(self, profession, valley):
        # 初始化函数，默认
        super(Auto, self).__init__()
        self.game = Game()
        self.recogbot = Recogbot()
        self.player = Player('Aorist')
        self.notification = Notification()

        self.profession = profession
        self.current_work = 'main'
        self.valley = valley
        self.workers = {}
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
        # 溪谷
        if self.valley:
            self.workers['valley'] = {}
            self.workers['valley']['thread'] = []
            v = ValleyWorker(self.game, self.recogbot)
            v.trigger.connect(self._working_stop)
            self.workers['valley']['thread'].append(v)

            f = PlayerFightWorker(self.game, self.recogbot, self.player)
            f.trigger.connect(self._working_stop)
            self.workers['valley']['thread'].append(f)

            s = PlayerSkillCooldownWorker(self.player)
            self.workers['valley']['thread'].append(s)

            a = PlayerAttackWorker(self.player)
            self.workers['valley']['thread'].append(a)
            self.workers['valley']['working'] = 0

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

    def _reset_work(self):
        self.current_work = 'main'
        for key in self.workers.keys():
            self.workers[key]['working'] = 0

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
        print(f"【Auto Work】停止{self.current_work}")
        for w in self.workers[self.current_work]['thread']:
            w.stop()
        self.workers[self.current_work]['working'] = 2
        self.player.over_fatigued()

    def _switch_player(self):
        next_player = self._next_piglet()
        self.game.switch(next_player, lambda player: (
            self._set_player(player), self._reset_work(), self._current_piglet_update(player),
            self._send(f"【{player}】开始工作")))

    def _fight(self):
        print(f"【Auto Work】开启{self.current_work}线程，当前角色{self.player}")
        for w in self.workers[self.current_work]['thread']:
            w.start()
        # 标识开始战斗
        self.workers[self.current_work]['working'] = 1

    def _next_work(self):
        keys = list(self.workers.keys())
        print(keys)
        index = keys.index(self.current_work)
        self.current_work = index and keys[index - 1] or None
        print(self.current_work)

    def _run(self):
        # 卡一行
        self.recogbot.town()
        if self.current_work is None and self.recogbot.town():
            self._switch_player()

        if self.current_work is not None and self.workers[self.current_work]['working'] == 0:
            self._fight()
        # 开启下个任务
        if self.current_work is not None and self.workers[self.current_work]['working'] == 2 and self.recogbot.town():
            print('开始执行下个任务')
            self._next_work()

    def run(self):
        print("【Auto Work】Auto Work开始执行")
        while True:
            self._run()

    def stop(self):
        print("【Auto Work】Auto Work停止执行")
        self._working_stop()
        self.terminate()
