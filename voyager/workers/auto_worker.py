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
        self.workers_queue = []

    def reset(self):
        self.worker = None
        self.working = False
        self.workers_queue = self.workers.copy()

    # 初始化配置，读取角色列表
    def _init_players(self):
        print("【探索者】读取角色配置")
        config = ConfigParser()
        config.read('conf/player.ini', encoding='UTF-8')
        players = config.sections()
        print("【探索者】读取到的角色", players)

        if self.profession == 'Strive' or self.profession == 'LevelUp':
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

    def finish(self, args):
        if self.worker is None:
            print(f"【自动任务】意外的线程结束：{args}")
            return

        if self.worker.__class__.__name__ == args:
            print("【自动任务】任务执行结束", args)
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
                self.trigger.emit(self.__class__.__name__)
                return
            next_player = self.players[i + 1]
        else:
            next_player = self.players[0]
        return next_player

    def send(self, message):
        print(f"【自动任务】{self.profession} {message}")
        self.voyager.notification.send(message)

    # 任务执行完成
    def continuous_run(self):
        if self.working:
            return

        cls = self.voyager.recogbot.detect()

        # 所有任务执行结束，人在地下城
        if len(self.workers_queue) == 0 and (cls['skill'][0] or cls['result'][0]):
            self.voyager.game.back_town(cls['setting'])

        # 所有任务执行结束，人在城镇，打开菜单
        if len(self.workers_queue) == 0 and self.voyager.recogbot.town() and not cls['switch'][0]:
            self.voyager.game.open_menu()

        # 所有任务执行结束，人在城镇，菜单已打开，选择角色
        if len(self.workers_queue) == 0 and cls['switch'][0]:
            self.voyager.game.switch_player(cls['switch'])

        # 选择角色页面
        if self.voyager.recogbot.start_game():
            next_player = self.next_player()

            if next_player is None:
                return

            def callback(next_player):
                self._current_player_update(next_player)
                self._init_player()
                self.reset()

            self.voyager.game.switch_find_player(next_player, callback)

        # 还有其他任务需要执行
        if len(self.workers_queue) > 0:
            # 等待上个任务完全停止
            self.sleep(5)
            self.worker = self.workers_queue.pop()
            self.worker.start()
            self.working = True
