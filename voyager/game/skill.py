from PyQt5.QtCore import QTimer

from voyager.control import click, press


class Skill:
    def __init__(self, key, cd):
        self.key = key
        self.cd = cd
        # 技能剩余冷却时间
        self.remain = 0
        # 技能CD计时器
        self.timer = QTimer()

    def __repr__(self):
        return '%s CD：%s' % (self.key, self.remain)

    def cast(self):
        print("释放技能", self.key)
        press(self.key.lower())
        self.remain = self.cd
        self.timer.start(1000)
        self.timer.timeout.connect(self._remaining)

    def remain(self):
        return self.remain

    def _remaining(self):
        if self.remain > 0:
            self.remain = self.remain - 1
        else:
            self.timer.stop()
