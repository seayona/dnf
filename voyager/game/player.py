import asyncio
import random
from configparser import ConfigParser

from voyager.control import keyUp, keyDown, press
from voyager.game import Skill
from voyager.infrastructure import idle, asyncthrows, Concurrency


class Player(Concurrency):

    def __init__(self, name):
        super().__init__()
        # 角色名称
        self.name = name
        # 祥瑞溪谷次数
        self.valley = 3
        # 疲劳值
        self.pl = 100
        # 福利
        self.welfare = {'union': False, 'revival_coin': False, 'achievement': False, 'mail': False}
        # 技能
        self.skills = {}
        # Buff
        self.buff = {}
        # 觉醒
        self.awake = None

        self.stand_status = False

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
        if not self.stand_status:
            keyUp('x')
            keyDown('x')

    def attack(self):
        self._attack()

    def attack_active(self):
        self.stand_status = False

    def cooldown(self):
        for s in self.skills.values():
            s.remaining()

    @idle
    @asyncthrows
    async def cast(self, key=None):
        await self._cast(key)
        self._attack()
        self._free()

    async def _cast(self, key=None):
        if key is None:
            skills = sorted(self.skills.values(), key=lambda s: s.remain)
            print(skills)
            await skills[0].cast_async()
        else:
            skill = self.skills[key]
            await skill.cast_async()

    def cast_random(self):
        s = random.choice(list(self.skills.keys()))
        self.skills[s].cast()
        self._attack()

    def cast_flush(self):
        for s in self.skills.values():
            s.cast()

    def stand(self):
        self.stand_status = True
        keyUp('x')
        press('x')

    def finisher(self):
        if self.awake is not None:
            print(f'【角色控制】准备释放觉醒 CD {self.awake.remain}')
            self.awake.cast()
            self.awake.cast()
            self._attack()

    @idle
    @asyncthrows
    async def right(self):
        keyDown('right')
        await asyncio.sleep(2)
        self.stop_right()
        self._free()

    def stop_right(self):
        keyUp('right')
        press('right')

    def tired(self):
        return self.pl == 0

    def shine(self):
        return self.valley == 0

    def over_fatigued(self):
        self.pl = 0

    def over_valley(self):
        self.valley = 0

    def over_welfare(self, scene):
        self.welfare[scene] = True

    # 自动释放buff
    def release_buff(self, key):
        self.buff[key].cast()

    @idle
    @asyncthrows
    async def dodge_direction(self, direction):
        keyDown(direction)
        await asyncio.sleep(0.5)
        press('v')
        await asyncio.sleep(0.2)
        press('v')
        await asyncio.sleep(0.2)
        keyUp(direction)
        self._free()

    @idle
    @asyncthrows
    async def slowly_hit(self):
        for _ in range(5):
            press('x')
            await asyncio.sleep(0.25)
        await self._cast()
        self._free()
