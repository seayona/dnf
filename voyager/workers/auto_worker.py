from abc import abstractmethod
from configparser import ConfigParser

from PyQt5.QtCore import QThread

from voyager.game import Player


class AutoWorker(QThread):
    CONF_PATH = './conf/auto.ini'

    def __init__(self, voyager, profession: str):
        super().__init__()
        self.voyager = voyager

        # 工作类型，用于选择角色
        self.profession = profession
        # 角色列表
        self.players = []
        self.workers = []

        self._init_players()
        self._init_player()

        self.worker = None
        self.working = False
        self.switching = False
        self.workers_queue = []

    def reset(self):
        self.worker = None
        self.working = False
        self.switching = False
        self.workers_queue = self.workers.copy()

    # 初始化配置，读取角色列表
    def _init_players(self):
        print("【探索者】读取角色配置")
        config = ConfigParser()
        config.read('conf/player.ini', encoding='UTF-8')
        players = config.sections()
        print("【探索者】读取到的角色", players)

        if self.profession == 'Work' or self.profession == 'LevelUp':
            self.players = list(filter(lambda p: config.get(p, 'Work') == self.profession, players))
        else:
            self.players = list(players)

    # 初始化角色
    def _init_player(self):
        player = self.current()
        if player is None or player not in self.players:
            player = self.players[0]
        # 更新配置
        self._current_player_update(player)
        # 初始化角色
        self.voyager.player = Player(player)
        self.voyager.show_message(f"角色【{player}】配置已加载")

    def _current_player_update(self, value):
        conf = ConfigParser()
        conf.read(self.CONF_PATH)
        conf.set(self.profession, 'Player', value)
        conf.write(open(self.CONF_PATH, "w"))

    def _switch_complete(self):
        self.switching = False

    def finish(self):
        if self.worker is not None:
            self.worker.stop()
        self.worker = None
        self.working = False

    # 获取当前正在工作的角色
    def current(self):
        conf = ConfigParser()
        conf.read(self.CONF_PATH)
        player = conf.get(self.profession, 'Player')
        return player

    def next_player(self):
        current = self.current()
        if current in self.players:
            i = self.players.index(current)
            if i + 1 == len(self.players):
                self.send("【自动任务】所有角色工作完成")
                # 重置配置
                self._current_player_update(self.players[0])
                self.trigger.emit('stop')
                return
            next_player = self.players[i + 1]
        else:
            next_player = self.players[0]
        return next_player

    def send(self, message):
        print(f"【自动任务】{self.profession} {message}")
        self.voyager.notification.send(message)

    def switch_player(self):
        next_player = self.next_player()
        self.switching = True

        def callback(next_player):
            self._current_player_update(next_player)
            self._init_player()
            self._switch_complete()
            self.reset()

        if next_player is not None:
            self.voyager.game.switch(next_player, callback)

    # 任务执行完成
    def continuous_run(self):
        if self.working:
            return

        # 所有任务执行结束
        if len(self.workers_queue) == 0:
            self.switch_player()

        # 还有其他任务需要执行
        if len(self.workers_queue) > 0:
            self.worker = self.workers_queue.pop()
            self.worker.start()
            self.working = True
