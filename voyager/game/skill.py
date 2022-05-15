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
        self.timer.timeout.connect(self._remaining)

    def __repr__(self):
        return '%s CD：%s' % (self.key, self.remain)

    def cast(self):
        print("释放技能", self.key)
        # if self.key == 'Y':
        #     press(self.key.lower())
        #     self.timer.singleShot(1000, lambda: press(self.key.lower()))
        #     self.timer.singleShot(2000, lambda: press(self.key.lower()))
        #     self.timer.singleShot(3000, lambda: press(self.key.lower()))
        # elif self.key == 'L':
        #     press(self.key.lower())
        #     self.timer.singleShot(1000, lambda: press('b'))
        # else:
        # 连按2次
        press(self.key.lower())
        press(self.key.lower())
        self.remain = self.cd
        self.timer.start(1000)

    def _remaining(self):
        if self.remain > 0:
            self.remain = self.remain - 1
        else:
            self.remain = 0
            self.timer.stop()
