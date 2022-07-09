import asyncio

from voyager.control import click, press, keyUp, keyDown
from voyager.infrastructure import idle, Concurrency, asyncthrows


class Skill():

    def __init__(self, key, cd):
        self.key = key
        self.cd = cd
        self.remain = 0

    def __repr__(self):
        return '%s CD：%s' % (self.key, self.remain)

    def cast(self):
        print("释放技能", self.key)
        press(self.key.lower())
        self.remain = self.cd

    @asyncthrows
    async def cast_async(self):
        if len(self.key) == 1:
            self.cast()
            return await asyncio.sleep(0)
        if self.key.__contains__('-'):
            for idx, s in enumerate(self.key.split('-')):
                if ((idx + 1) % 2) == 1:
                    print(f"【技能】释放组合技能[{self.key}]  {s}")
                    press(s)
                if ((idx + 1) % 2) == 0:
                    await asyncio.sleep(float(s))

        if self.key.__contains__('#'):
            hold_skill = self.key.split('#')
            keyDown(hold_skill[0])
            await asyncio.sleep(0.3)
            keyDown(hold_skill[1])
            await asyncio.sleep(0.3)
            keyUp(hold_skill[0])
            await asyncio.sleep(0.3)
            keyUp(hold_skill[1])

        if self.key.__contains__('*'):
            s = self.key.split('*')
            keyDown(s[0])
            await asyncio.sleep(float(s[1]))
            keyUp(s[0])

        self.remain = self.cd

    def remaining(self):
        if self.remain > 0:
            self.remain = self.remain - 1
        else:
            self.remain = 0

    def reset_cooldown(self):
        self.remain = 0
