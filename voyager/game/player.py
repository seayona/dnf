import functools
import random
import time

from PyQt5.QtCore import QTimer

from voyager.control import keyUp, keyDown, press, moveTo, click
from voyager.game import Skill
from voyager.recognition import Recogbot


class Player(object):
    # 白手
    # Skills = {
    #     'E': Skill('E', 38),
    #     'O': Skill('O', 19),
    #     'U': Skill('U', 19),
    #     'Q': Skill('Q', 19),
    #     'Y': Skill('Y', 5),
    #     'F': Skill('F', 19),
    #     'B': Skill('B', 5),
    #     'L': Skill('L', 5),
    #     '6': Skill('6', 57)
    # }
    # 红眼
    # Skills = {
    #     'E': Skill('E', 40),
    #     'O': Skill('O', 12),
    #     'U': Skill('U', 20),
    #     'Q': Skill('Q', 20),
    #     'Y': Skill('Y', 20),
    #     'F': Skill('F', 22),
    #     'B': Skill('B', 6),
    #     'L': Skill('L', 6),
    #     '6': Skill('6', 60)
    # }
    # 瞎子
    Skills = {
        'A': Skill('A', 5),
        'S': Skill('S', 7),
        'D': Skill('D', 10),
        'F': Skill('F', 20),
        'Q': Skill('Q', 20),
        'W': Skill('W', 22),
        'R': Skill('R', 6),
        'T': Skill('T', 140),
        '3': Skill('3', 60),
        'V': Skill('V', 1)
    }
    Finisher = Skill('3', 140)

    def __init__(self):
        self.recogbot = Recogbot()

        self.ready = False
        self.timer = QTimer()
        self.timer.timeout.connect(self._attack)

    def _attack(self):
        print("自动攻击")
        keyUp('x')
        keyDown('x')

    def cast(self):
        skills = sorted(self.Skills.values(), key=lambda s: s.remain)
        print(skills)
        skills[0].cast()
        # s = random.choice(list(self.Skills.keys()))
        # self.Skills[s].cast()
        self._attack()

    def stand(self):
        keyUp('x')
        self.timer.stop()

    def attack(self):
        self.timer.start(3200)

    def finisher(self):
        print(f'【角色控制】准备释放觉醒 CD {self.Finisher.remain}')
        self.Finisher.cast()
        self._attack()

    def right(self):
        keyDown('right')
        self.timer.singleShot(3200, lambda: self.attack())
