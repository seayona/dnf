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
        self.saled = False
        self.lionAlive = True

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

    def _onsaled(self):
        self.saled = True
        print('【探索者】装备分解完成')

    async def _click(self, target, sleep=1):
        top_left = self._archor(target)
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            await asyncio.sleep(sleep)

    async def _press(self, key, sleep=1):
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

    def lion_clear(self):
        self.lionAlive = False

    @idle
    async def sale(self):
        if self.saled:
            print("【探索者】装备已分解，无需分解")
            return
        # 打开背包
        await self._click('bag')
        # 点击分解按钮
        await self._click('sale')
        # 确认分解
        await self._click('sale_select')
        # 确认分解
        await self._click('sale_confirm')
        # 返回！
        await self._press('esc')
        # 返回！
        await self._press('esc')
        # 返回！
        await self._press('esc')
        # 标记修理状态
        self._onsaled()
    @idle
    async def talk_skip(self):
        await self._click('talk_skip')
    @idle
    async def confirm(self):
        await self._click('confirm')

    @idle
    async def agency_mission(self):
        pass

    @idle
    async def agency_mission_finish(self):
        # 返回！
        await self._press('esc')
        # 返回！
        await self._press('esc')
        # 返回！
        await self._click('adventure_snow_mountain_town')


    @idle
    async def next(self):
        await self._click('next')

    @idle
    async def next_agency(self):
        top_left = self._archor('next_agency')
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x + 40, y + 6)
    @idle
    async def next_agency_confirm(self):
        await self._click('next_agency_confirm')

    @idle
    async def equip(self):
        await self._click('equip')

    @idle
    async def click_close(self):
        await self._click('click_close')

    @idle
    async def back(self):
        await self._click('back')

