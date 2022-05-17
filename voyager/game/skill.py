from PyQt5.QtCore import QTimer

from voyager.control import click, press


class Skill:
    def __init__(self, key, cd):
        self.key = key
        self.cd = cd
        self.remain = 0

    def __repr__(self):
        return '%s CD：%s' % (self.key, self.remain)

    def cast(self):
        print("释放技能", self.key)
        press(self.key.lower())
        press(self.key.lower())
        self.remain = self.cd

    def remaining(self):
        if self.remain > 0:
            self.remain = self.remain - 1
        else:
            self.remain = 0
