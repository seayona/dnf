import functools
import random
import time
from configparser import ConfigParser

from voyager.control import keyUp, keyDown, press, moveTo, click, hold
from voyager.game import Skill


class Player(object):

    def __init__(self, name):
        self.name = name
        self.pl = 100
        self.skills = {}
        self._init_skills(name)

    def _init_skills(self, name):
        conf = ConfigParser()
        conf.read('./conf/player.ini', encoding='UTF-8')
        skills = eval(conf.get(name, 'Skills'))
        for s in skills:
            self.skills[s[0]] = Skill(str(s[0]), s[1])
        s = eval(conf.get(name, 'Awake'))
        self.awake = Skill(str(s[0]), s[1])

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
        print(f'【角色控制】准备释放觉醒 CD {self.awake.remain}')
        self.awake.cast()
        self.awake.cast()
        self._attack()

    def right(self):
        keyUp('right')
        press('v')
        press('v')
        keyDown('right')

    def tired(self):
        return self.pl == 0

    def over_fatigued(self):
        self.pl = 0
