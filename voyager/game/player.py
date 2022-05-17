import functools
import random
import time

from PyQt5.QtCore import QTimer

from voyager.control import keyUp, keyDown, press, moveTo, click, hold
from voyager.game import Skill
from voyager.recognition import Recogbot


class Player(object):
    final_skill = Skill('3', 140)
    skills = {
        'E': Skill('E', 38),
        'O': Skill('O', 19),
        'U': Skill('U', 19),
        'Q': Skill('Q', 19),
        'Y': Skill('Y', 5),
        'F': Skill('F', 19),
        'B': Skill('B', 5),
        'L': Skill('L', 5),
        '6': Skill('6', 57)
    }

    def __init__(self, role):
        self.role = role
        self._init_skills()

    def _init_skills(self):
        if self.role == 'blademaster':
            self.skills = {
                '6': Skill('6', 20),
                'E': Skill('E', 38),
                'O': Skill('O', 22),
                'U': Skill('U', 22),
                'F': Skill('F', 22),
                'Q': Skill('Q', 12),
                'Y': Skill('Y', 5),
                'B': Skill('B', 5),
                'L': Skill('L', 5),
            }
            self.final_skill = Skill('3', 140)
        elif self.role == 'berserker':
            self.skills = {
                '6': Skill('6', 20),
                '5': Skill('5', 20),
                'E': Skill('E', 40),
                'U': Skill('U', 20),
                'Q': Skill('Q', 20),
                'Y': Skill('Y', 20),
                'F': Skill('F', 22),
                'O': Skill('O', 12),
                'B': Skill('B', 6),
                'L': Skill('L', 6)
            }
            self.final_skill = Skill('3', 140)
        elif self.role == 'asura':
            self.skills = {
                'Q': Skill('Q', 20),
                'O': Skill('O', 6),
                'E': Skill('O', 5),
                # '3': Skill('3', 5),
                # 'F': Skill('F', 20),
                # 'W': Skill('W', 22),xx
                # 'S': Skill('S', 7),
                # 'R': Skill('R', 6),
                # 'A': Skill('A', 5),
                # 'V': Skill('V', 1)
            }
            self.final_skill = Skill('T', 140)

    def _attack(self):
        keyUp('x')
        keyDown('x')

    def attack(self):
        self._attack()

    def cooldown(self):
        for s in self.skills.values():
            s.remaining()

    def cast(self):
        skills = sorted(self.skills.values(), key=lambda s: s.remain)
        print(skills)
        skills[0].cast()
        self._attack()

    def cast_random(self):
        s = random.choice(list(self.skills.keys()))
        self.skills[s].cast()
        self._attack()

    def cast_flush(self):
        for s in self.skills.values():
            s.cast()

    def stand(self):
        press('x')
        press('v')

    def finisher(self):
        print(f'【角色控制】准备释放觉醒 CD {self.final_skill.remain}')
        self.final_skill.cast()
        self.final_skill.cast()
        self._attack()

    def right(self):
        keyUp('right')
        press('v')
        press('v')
        keyDown('right')
