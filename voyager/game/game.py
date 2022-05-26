import asyncio

from voyager.control import click, press, keyUp, keyDown
from voyager.infrastructure import Concurrency, idle, asyncthrows
from voyager.recognition import capture, match


class Game(Concurrency):

    def __init__(self):
        super().__init__()

        self.freezy = True

        self.repaired = False
        self.lionAlive = True

    def _archor(self, target, img=None):
        if img is None:
            img = capture()
        # 检测再次挑战的按钮位置
        max_val, img, top_left, right_bottom = match(img, './game/scene/' + target + '.png')
        print(f'【模板匹配】{target} {max_val} {top_left}')
        if top_left[0] == 0 and top_left[1] == 0:
            return False
        if 1 >= max_val > 0.99:
            x, y = top_left
            # 返回按钮位置
            return x + 10, y + 8

    def _archor_low_precision(self, target, img=None):
        # 获取屏幕截图
        if img is None:
            img = capture()
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, f'./game/scene/{target}.png')
        print(f'【模板匹配】{target} {max_val} {top_left}')
        # 返回按钮位置
        if 1 >= max_val > 0.94:
            x, y = top_left
            return x + 10, y + 8

    async def _click(self, target, sleep=1, img=None):
        top_left = self._archor(target, img)
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            await asyncio.sleep(sleep)

    async def _click_xy(self, x, y, sleep=1):
        # 移动鼠标到按钮位置,点击按钮
        click(x, y)
        await asyncio.sleep(sleep)

    async def _click_if(self, target1, target2, sleep=1, img=None):
        top_left = self._archor(target1, img)
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            await asyncio.sleep(sleep)
            return
        top_left = self._archor(target2, img)
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            await asyncio.sleep(sleep)

    async def _click_low_precision(self, target, sleep=1, img=None):
        top_left = self._archor_low_precision(target, img)
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            await asyncio.sleep(sleep)

    async def _double_click_low_precision(self, target, sleep=1, img=None):
        top_left = self._archor_low_precision(target, img)
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            click(x, y)
            await asyncio.sleep(sleep)

    async def _double_click(self, target, sleep=1, img=None):
        top_left = self._archor(target, img)
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            click(x, y)
            await asyncio.sleep(sleep)

    async def _press(self, key, sleep=1.5):
        press(key)
        await asyncio.sleep(sleep)

    async def _print(self, message, sleep=1.5):
        print(message)
        await asyncio.sleep(sleep)

    async def _player_switch(self, target):
        top_left = self._archor_low_precision(target)
        if top_left:
            x, y = top_left
            # 选中
            click(x, y)
            # 开始按钮可靠性更高
            click(x, y)
            click(x, y)
            click(x, y)
            click(x, y)

    async def _player_switch_next(self):
        # 创建角色向上便宜40个像素，翻到第二页
        top_left = self._archor('player_create')
        if top_left:
            # 选中
            x, y = top_left
            click(x - 10, y - 48)
        top_left = self._archor('player_create_grey')
        if top_left:
            # 选中
            x, y = top_left
            click(x - 10, y - 48)

    def reset(self):
        self.repaired = False
        self.lionAlive = True

    def lion_clear(self):
        self.lionAlive = False

    @idle
    @asyncthrows
    async def printf(self):
        await self._print('开始打印')
        for i in range(5):
            await self._print(f'第{i}次打印')
        self._free()

    @idle
    @asyncthrows
    async def replay(self):
        self.reset()
        await self._click_if('replay', 'replay_kr')
        await self._click_if('confirm', 'confirm_kr')
        print('【探索者】开始再次挑战')
        self._free()

    @idle
    @asyncthrows
    async def reward(self):
        await self._click('gold')
        await self._click('gold2')
        print('【探索者】战斗结束，领取奖励完成')
        self._free()

    @idle
    @asyncthrows
    async def repair_and_sale(self, bag=(False, 0, 0)):
        if self.repaired:
            print("【探索者】已修理，无需修理")
            self._free()
            return

        # 打开背包，防止识别到城镇中下面的那个背包
        if bag[0]:
            await self._click_xy(bag[1] + 10, bag[2] + 8)
        else:
            await self._click('bag')

        # 点击修理按钮
        await self._click('repair')
        # 确认修理
        await self._click_if('repair_confirm', 'repair_confirm_kr')
        # 返回！
        await self._press('esc')

        await self._sale()
        # 标记修理状态
        self.repaired = True
        print('【探索者】装备修理完成')
        self._free()

    @asyncthrows
    async def _sale(self):
        # 点击分解按钮
        await self._click('sale')
        # 确认分解
        await self._click_if('sale_select', 'sale_select_kr')
        # 确认分解
        await self._click('sale_confirm')
        # 返回！
        await self._press('esc')
        # 返回！
        await self._press('esc')
        # 执行售卖
        await self._click('sell')
        # 确认售卖
        await self._click_if('sell_select', 'sell_select_kr')
        # 确认分解,按钮与分解一毛一样
        await self._click('sale_confirm')
        # 确认分解
        # 返回！
        await self._press('esc')
        # 返回！
        await self._press('esc')
        # 返回！
        await self._press('esc')
        print('【探索者】装备分解完成')

    @idle
    @asyncthrows
    async def revival(self):
        await self._click_if('revival', 'revival_kr')
        print('【探索者】原地复活！消耗复活币1枚')
        self._free()

    @idle
    @asyncthrows
    async def valley_start(self):
        if not self._archor('mail'):
            await self._press('esc')
        await self._click('active')
        await self._click('daily')
        print('【探索者】打开日常界面')
        self._free()

    @idle
    @asyncthrows
    async def valley_fight(self):
        await self._click('valley')
        await self._click_if('valley_confirm', 'valley_confirm_kr')
        print('【探索者】开始挑战祥瑞溪谷')
        self._free()

    @idle
    @asyncthrows
    async def valley_town(self):
        # 等待碎片捡完
        await asyncio.sleep(3)
        await self._click_if('valley_town', 'valley_town_kr')
        print('【探索者】祥瑞溪谷结束，回到城镇')
        self._free()

    @idle
    @asyncthrows
    async def snow_mountain_start(self, callback):
        await asyncio.sleep(5)
        print("【探索者】前往雪山")
        await self._click('active')
        await self._click('adventure_box')
        await self._click('adventure_hard_level')
        await self._click('adventure_snow_mountain')
        await self._click('adventure_go')
        print('【探索者】抵达雪山')
        callback()
        self._free()

    @idle
    @asyncthrows
    async def snow_mountain_fight(self):
        await self._click('adventure_snow_mountain_hard')
        await self._click('adventure_snow_mountain_entry')
        await self._click('adventure_snow_mountain_confirm')
        print('【探索者】开始雪山搬砖')
        self._free()

    @idle
    @asyncthrows
    async def snow_mountain_finish(self):
        await self._press('esc')
        await self._click('adventure_snow_mountain_town')
        print('【探索者】雪山搬砖完成，下班！')
        self._free()

    @idle
    @asyncthrows
    async def confirm(self):
        await self._click_if('confirm', 'confirm_kr')
        print('【探索者】确认！')
        self._free()

    @idle
    @asyncthrows
    async def agency_mission(self):
        self._free()

    @idle
    @asyncthrows
    async def agency_mission_finish(self):
        # 返回！
        await self._press('esc')
        # 返回！
        await self._press('esc')
        # 返回！
        await self._click_if('adventure_snow_mountain_town', 'adventure_snow_mountain_town_kr')
        print('【探索者】结束任务，返回城镇！')
        self._free()

    @idle
    @asyncthrows
    async def next(self, next):
        if next[0]:
            click(next[1] + 10, next[2] + 8)
            print('【探索者】剧情下个主线任务')
        self._free()

    @idle
    @asyncthrows
    async def next_agency(self):
        top_left = self._archor('running')
        if top_left:
            print('【探索者】正在自动寻路')
            self._free()
            return
        top_left = self._archor('next_agency')
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x + 40, y + 6)
        print('【探索者】下个主线任务')
        self._free()

    @idle
    @asyncthrows
    async def next_agency_confirm(self):
        self.reset()
        await self._click('next_agency_confirm')
        print('【探索者】下个主线任务')
        self._free()

    @idle
    @asyncthrows
    async def equip(self):
        await self._click_if('equip', 'equip_kr')
        print('【探索者】自动装备')
        self._free()

    @idle
    @asyncthrows
    async def click_close(self):
        await self._click('click_close')
        print('【探索者】点击关闭')
        self._free()

    @idle
    @asyncthrows
    async def back(self):
        await self._click('back')
        print('【探索者】返回界面')
        self._free()

    @idle
    @asyncthrows
    async def esc(self):
        print("【取消操作】ESC")
        await self._press('esc')
        self._free()

    @idle
    @asyncthrows
    async def switch(self, player, callback):
        await self._press('esc')
        # 选择角色
        await self._click('switch')
        # 等待7秒加载选择角色界面
        await asyncio.sleep(7)
        # 选择角色
        target = 'players/' + player
        top_left = self._archor_low_precision(target)
        if top_left:
            await self._player_switch(target)
            self._free()
            callback(player)
            return
        print('【选择角色】第一页没找到，翻到第二页')
        # 翻到第二页
        await self._player_switch_next()
        await asyncio.sleep(1.5)
        top_left = self._archor_low_precision(target)
        if top_left:
            await self._player_switch(target)
            self._free()
            callback(player)
            return

        print('【选择角色】第二页没找到，翻到第三页')
        # 翻到第三页
        await self._player_switch_next()
        await asyncio.sleep(1.5)
        top_left = self._archor_low_precision(target)
        if top_left:
            await self._player_switch(target)
            self._free()
            callback(player)
            return
        self._free()

    @idle
    @asyncthrows
    async def agency_mission_confirm(self):
        await self._click_if('agency_mission_confirm', 'agency_mission_confirm_kr')
        print('【探索者】没有主线任务了，打怪升级去')
        self._free()

    @idle
    @asyncthrows
    async def replay_agency(self):
        await self._click_if('replay', 'replay_kr')
        await self._click_if('confirm', 'confirm_kr')
        print('【探索者】没有主线任务了，打怪升级去')
        self._free()

    @idle
    @asyncthrows
    async def agency_mission_get(self):
        await self._click_if('agency_mission_get', 'agency_mission_get_kr')
        print('【探索者】接受酒馆任务')
        self._free()

    @idle
    @asyncthrows
    async def town(self):
        # 如果在地下城中，已通关
        top_left = self._archor('result')
        if top_left:
            await self._click_if('adventure_snow_mountain_town', 'adventure_snow_mountain_town_kr')
            # 等待返回城镇
            await asyncio.sleep(5)
            self._free()
            return

        # 如果在地下城中
        top_left = self._archor_low_precision('setting')
        if top_left:
            await self._click_low_precision('setting')
            await self._click('home')
            await self._click_if('confirm', 'confirm_kr')
            # 等待返回城镇
            await asyncio.sleep(5)
            self._free()
            return

        # 如果在城镇中，但是看不到邮箱按钮，尝试按一次esc
        top_left = self._archor('mail')
        if not top_left:
            await self._press('esc')

        # 选关卡页面或者背包等二级页面
        top_left = self._archor('asset')
        if not top_left:
            await self._press('esc')

        # 选关卡待确认页面
        top_left = self._archor('close')
        if not top_left:
            await self._press('esc')

    @idle
    @asyncthrows
    async def sky_mission_receive(self):
        await self._click('sky_mission_receive')
        print('【探索者】天界任务领取')
        self._free()

    async def _key_hold(self, key, holding=1):
        keyDown(key)
        await asyncio.sleep(holding)
        keyUp(key)

    @idle
    @asyncthrows
    async def out_stuck(self, direction):
        await self._key_hold(direction)
        print('【探索者】正在脱困')
        self._free()
