import functools
import random
import time
from configparser import ConfigParser

from voyager.control import keyUp, keyDown, press, moveTo, click, hold
from voyager.game import Skill
from voyager.infrastructure import idle, asyncthrows, Concurrency
from voyager.recognition import Recogbot


class Player(Concurrency):

    def __init__(self, name):
        super().__init__()
        self.name = name
        self.pl = 100
        self.skills = {}
        self.buff = {}
        self.awake = None
        self.recogbot = Recogbot()
        self._init_skills(name)

    def _init_skills(self, name):
        conf = ConfigParser()
        conf.read('./conf/player.ini', encoding='UTF-8')
        skills = eval(conf.get(name, 'Skills'))
        for s in skills:
            self.skills[s[0]] = Skill(str(s[0]), s[1])
        if conf.has_option(name, 'Awake'):
            s = eval(conf.get(name, 'Awake'))
            self.awake = Skill(str(s[0]), s[1])
        if conf.has_option(name, 'Buffs'):
            buffs = eval(conf.get(name, 'Buffs'))
            for b in buffs:
                self.buff[b[1]] = Skill(str(b[0]), 0)

    def _attack(self):
        keyUp('x')
        keyDown('x')

    def attack(self):
        self._attack()

    def cooldown(self):
        for s in self.skills.values():
            s.remaining()

    @idle
    @asyncthrows
    async def cast(self, s=None):
        if s is None:
            skills = sorted(self.skills.values(), key=lambda s: s.remain)
            print(skills)
            await skills[0].cast_async()
        else:
            skill = self.skills[s]
            await skill.cast_async()
        self._attack()
        self._free()

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
        if self.awake is not None:
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

    # 自动释放buff
    def release_buff(self, key):
        self.buff[key].cast()
