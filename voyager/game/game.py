import asyncio

from PyQt5.QtCore import QTimer

from voyager.control import moveTo, click, press
from voyager.recognition import capture, match, Recogbot


def idle(fn):
    def _freeze(*args):
        self = args[0]
        if self.freezy:
            print(f'【探索者】开始执行系统任务 {fn.__name__}')
            self.freezy = False
            asyncio.run(fn(self))
            self._free()

    return _freeze


class Game(object):
    def __init__(self):
        self.freezy = True
        self.recogbot = Recogbot()
        self.timer = QTimer()

        self._init()

    def _init(self):
        self.repaired = False

    def _archor(self, target):
        # 获取屏幕截图
        img = capture()
        # 检测再次挑战的按钮位置
        max_val, img, top_left, right_bottom = match(img, './game/scene/' + target + '.png')
        if 1 >= max_val > 0.99:
            # 返回按钮位置
            x, y = top_left
            return x + 10, y + 8

    def _free(self):
        print('【探索者】系统空闲')
        self.freezy = True

    def _onrepaired(self):
        self.repaired = True
        print('【探索者】装备修理完成')

    async def _click(self, target, sleep=1.5):
        top_left = self._archor(target)
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            await asyncio.sleep(sleep)

    async def _press(self, key, sleep=1.5):
        press(key)
        await asyncio.sleep(sleep)

    @idle
    async def replay(self):
        self._init()

        await self._click('replay')
        await self._click('confirm')
        print('【探索者】开始再次挑战')

    @idle
    async def reward(self):
        await self._click('gold')
        await self._click('gold2')
        print('【探索者】战斗结束，领取奖励完成')

    @idle
    async def repair(self):
        if self.repaired:
            print("【探索者】已修理，无需修理")
            return

        # 打开背包
        await self._click('bag')
        # 点击修理按钮
        await self._click('repair')
        # 确认修理
        await self._click('repair_confirm')
        # 返回！
        await self._press('esc')
        # 返回！
        await self._press('esc')
        # 返回！
        await self._press('esc')
        # 标记修理状态
        self._onrepaired()

    @idle
    async def revival(self):
        await self._click('revival')

    @idle
    async def valley_start(self):
        if not self._archor('charge'):
            await self._press('esc')
        await self._click('active')
        await self._click('daily')

    @idle
    async def valley_fight(self):
        await self._click('valley')
        await self._click('valley_confirm')

    @idle
    async def valley_town(self):
        # 等待碎片捡完
        await asyncio.sleep(3)
        await self._click('valley_town')

    @idle
    async def snow_mountain_start(self):
        if not self._archor('charge'):
            press('esc')
        await self._click('active')
        await self._click('adventure_box')
        await self._click('adventure_hard_level')
        await self._click('adventure_snow_mountain')
        await self._click('adventure_go')

    @idle
    async def snow_mountain_fight(self):
        await self._click('adventure_snow_mountain_hard')
        await self._click('adventure_snow_mountain_entry')
        await self._click('adventure_snow_mountain_confirm')

    @idle
    async def snow_mountain_finish(self):
        print('【探索者】雪山搬砖完成，下班！')
        await self._press('esc')
        await self._click('adventure_snow_mountain_town')
