from PyQt5.QtCore import QThread, pyqtSignal
from .welfare_guild import WelfareGuild


class Welfare(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, game, recogbot, ):
        super(Welfare, self).__init__()

        self.game = game
        self.recogbot = recogbot

        self.current_work = 0
        self.works = []
        self._init_work()

    # 初始化任务
    def _init_work(self):
        # 公会签到
        w = WelfareGuild(self.game, self.recogbot)
        w.trigger.connect(self._current_work_complete)

        # 商城复活币

        # 每日

        # 添加到队列
        self.works.appnd({'thread': [w], 'working': 0})

    # 所有任务完成
    def _all_work_complete(self):
        self.trigger.emit(str('stop'))

    def _current_work_complete(self):
        self.works[self.current_work]['working'] = 2

    def _work_start(self):
        for w in self.works[self.current_work]['thread']:
            w.start()
        self.works[self.current_work]['working'] = 1

    def _next_work(self):
        if len(self.works) <= self.current_work + 1:
            self.current_work = -1
        else:
            self.current_work += 1

    def _run(self):
        if self.current_work == -1:
            self._all_work_complete()
            return
        if self.works[self.current_work]['working'] == 2:
            self._next_work()

        if self.works[self.current_work]['working'] == 0:
            print('开始任务')
            self._work_start()

    def run(self):
        print("【探索者】福利领取开始执行", int(QThread.currentThreadId()))
        while True:
            self._run()

    def stop(self):
        print("【探索者】福利领取停止执行")
        self._working_stop()
        self.terminate()
