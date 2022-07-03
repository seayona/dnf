import asyncio
import math
from voyager.control import click, press, keyUp, keyDown
from voyager.infrastructure import Concurrency, idle, asyncthrows
from voyager.recognition import capture, match, match_best


class Game(Concurrency):

    def __init__(self):
        super().__init__()
        self.freezy = True

    def _archor(self, target, img=None, debug=False):
        return self._archor_diy_precision(target, 0.99, img, debug)

    def _archor_if(self, target1, target2, img=None, debug=False):
        return self._archor(target1, img, debug) or self._archor(target2, img, debug)

    def _archor_best(self, target, img=None, debug=False):
        if img is None:
            img = capture()
        # 检测再次挑战的按钮位置
        max_val, img, top_left, right_bottom = match_best(img, './game/scene/' + target + '.png', debug)
        print(f'【模板匹配RGB】{target} {max_val} {top_left}')
        if top_left[0] == 0 and top_left[1] == 0:
            return False
        if 1 >= max_val > 0.99:
            x, y = top_left
            # 返回按钮位置
            return x + 10, y + 8

    def _archor_low_precision(self, target, img=None):
        return self._archor_diy_precision(target, 0.94, img)

    def _archor_diy_precision(self, target, precision, img=None, debug=False):
        # 获取屏幕截图
        if img is None:
            img = capture()
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, f'./game/scene/{target}.png', debug)
        print(f'【archor模板匹配】{target} {max_val} {top_left}')
        # 返回按钮位置
        if 1 >= max_val > precision:
            x, y = top_left
            return x + 10, y + 8

    def _archor_low_precision_if(self, target, target2, img=None):
        return self._archor_low_precision(target, img) or self._archor_low_precision(target2, img)

    async def _click(self, target, sleep=1, img=None, max_try=False):
        top_left = self._archor(target, img)
        max_try = 900 if max_try > 900 or (isinstance(max_try, bool) and max_try) else max_try
        if max_try and not top_left:
            print(f'【任务调度】{target}这个按钮很重要，必须点击，继续尝试')
            max_try -= 1
            return await self._click(target, sleep, img, max_try)
        return await self._click_event(top_left, sleep)

    async def _click_event(self, top_left, sleep):
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            await asyncio.sleep(sleep)
            return True
        return False

    async def _click_diy_precision(self, target, precision, sleep=1, img=None, max_try=False):
        top_left = self._archor_diy_precision(target, precision, img)
        max_try = 900 if max_try > 900 or (isinstance(max_try, bool) and max_try) else max_try
        if max_try and not top_left:
            print(f'【任务调度】{target}这个按钮很重要，必须点击，继续尝试')
            max_try -= 1
            return await self._click(target, sleep, img, max_try)

        return await self._click_event(top_left, sleep)

    async def _click_diy_precision_if(self, target1, target2, precision, sleep=1, img=None, max_try=False):
        result1 = await self._click_diy_precision(target1, precision, sleep, img, max_try)
        if not result1:
            await self._click(target2, precision, sleep, img, max_try)

    async def _click_xy(self, x, y, sleep=1):
        # 移动鼠标到按钮位置,点击按钮
        click(x + 10, y + 8)
        await asyncio.sleep(sleep)

    async def _click_if(self, target1, target2, sleep=1, img=None, max_try=False):
        result1 = await self._click(target1, sleep, img, max_try)
        if not result1:
            await self._click(target2, sleep, img, max_try)

    async def _click_low_precision(self, target, sleep=1, img=None, max_try=False):
        top_left = self._archor_low_precision(target, img)
        max_try = 900 if max_try > 900 or (isinstance(max_try, bool) and max_try) else max_try
        if max_try and not top_left:
            print(f'【任务调度】{target}这个按钮很重要，必须点击，继续尝试')
            max_try -= 1
            return await self._click_low_precision(target, sleep, img, max_try)
        return await self._click_event(top_left, sleep)

    async def _click_if_low_precision(self, target1, target2, sleep=1, img=None, max_try=False):
        result1 = await self._click_low_precision(target1, sleep, img, max_try)
        if not result1:
            await self._click_low_precision(target2, sleep, img, max_try)

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
            # 选中[
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

    @idle
    @asyncthrows
    async def printf(self):
        await self._print('开始打印')
        for i in range(5):
            await self._print(f'第{i}次打印')
        self._free()

    @idle
    @asyncthrows
    async def replay(self, reset):
        reset()
        await asyncio.sleep(4)
        await self._press('F6', 2)
        await self._click_if('confirm', 'confirm_kr')
        print('【探索者】开始再次挑战')
        self._free()

    @idle
    @asyncthrows
    async def daily_replay(self):
        await asyncio.sleep(3)
        await self._press('F6', 2)
        await self._click_if('confirm', 'confirm_kr')
        print('【探索者】开始再次挑战')
        self._free()

    @idle
    @asyncthrows
    async def reward(self, reset):
        reset()
        await self._click('gold')
        await self._click('gold2')
        print('【探索者】战斗结束，领取奖励完成')
        self._free()

    @idle
    @asyncthrows
    async def repair_and_sale(self, bag=(False, 0, 0), auto_back=True, callback=False):

        # 打开背包，防止识别到城镇中下面的那个背包
        if bag[0]:
            await self._click_xy(bag[1] + 10, bag[2] + 8, 2)
        else:
            await self._click('bag', 2)

        # 点击修理按钮
        await self._click_diy_precision('repair', 0.955, 2)
        # 确认修理
        await self._click_diy_precision_if('repair_confirm', 'repair_confirm_kr', 0.955, 2)
        # 返回！
        await self._click_diy_precision('close', 0.955, 2)

        await self._sale(auto_back)
        # 标记修理状态
        print('【探索者】装备修理完成')
        if callback:
            callback()
        self._free()

    @asyncthrows
    async def _sale(self, auto_back):
        # 点击分解按钮
        await self._click_diy_precision('sale', 0.955, 2)
        # 确认分解
        await self._click_diy_precision_if('sale_select', 'sale_select_kr', 0.955, 2)
        # 确认分解
        await self._click_diy_precision('sale_confirm', 0.955, 2)
        # 确认
        await self._click_diy_precision_if('confirm', 'confirm_kr', 0.955, 2)
        # 返回！
        await self._click_diy_precision('close', 0.955, 2)
        # 执行售卖
        await self._click_diy_precision('sell', 0.955, 2)
        # 确认售卖
        await self._click_diy_precision_if('sell_select', 'sell_select_kr', 0.955, 2)
        # 确认分解,按钮与分解一毛一样
        await self._click_diy_precision('sale_confirm', 0.955, 2)
        # 确认
        await self._click_diy_precision_if('confirm', 'confirm_kr', 0.955, 2)
        # 返回！
        await self._click_diy_precision('close', 0.955, 2)
        # 返回！
        if auto_back:
            await self._click('back', max_try=True)

        print('【探索者】装备分解完成')

    @idle
    @asyncthrows
    async def revival(self):
        await self._click_if('revival', 'revival_kr')
        print('【探索者】原地复活！消耗复活币1枚')
        self._free()

    @idle
    @asyncthrows
    async def daily_start(self):
        await asyncio.sleep(2)
        await self._click('active')
        await self._click('daily', 0)
        print('【探索者】打开日常界面')
        self._free()

    @idle
    @asyncthrows
    async def daily_fight(self, daily_type):
        await self._click(daily_type)
        print(f'【探索者】开始挑战每日任务：{daily_type}')
        self._free()

    @idle
    @asyncthrows
    async def daily_confirm(self):
        await self._click_if('valley_confirm', 'valley_confirm_kr')
        self._free()

    @idle
    @asyncthrows
    async def daily_town(self, wait=3, daily_next=False):
        # 等待碎片捡完
        await asyncio.sleep(wait)
        if daily_next:
            await self._press('F7')
        else:
            await self._press('F8')
        print('【探索者】日常结束，回到城镇')
        self._free()

    @idle
    @asyncthrows
    async def snow_mountain_start(self, reset):
        await asyncio.sleep(2)
        reset()
        print("【探索者】前往雪山")
        await self._click('active', 2)
        await self._click('adventure_box')
        await self._click('adventure_hard_level')
        await self._click('adventure_snow_mountain')
        await self._click('adventure_go')
        print('【探索者】抵达雪山')
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
    async def confirm(self):
        await self._click_if('confirm', 'confirm_kr', 0.5)
        await self._click_if('confirm2', 'confirm2_kr', 0.5)
        print('【探索者】确认！')
        self._free()

    @idle
    @asyncthrows
    async def agency_mission(self):
        self._free()

    @idle
    @asyncthrows
    async def agency_mission_finish(self, reset):
        reset()
        await self._click('close')
        await self._click('back')
        print('【探索者】结束任务，返回城镇！')
        await asyncio.sleep(5)
        self._free()

    @idle
    @asyncthrows
    async def next(self, next, reset):
        reset()
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
    async def close(self):
        await self._click('close')
        await self._click('close2')
        await self._click('close3')
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
    async def open_menu(self):
        await self._open_menu()
        self._free()

    async def _open_menu(self):
        # 点击菜单
        top_left = self._archor_low_precision('activity')
        if top_left:
            x, y = top_left
            await self._click_xy(x + 120, y)

    @idle
    @asyncthrows
    async def skill_back(self):
        await self._click("skill_back")
        self._free()

    @idle
    @asyncthrows
    async def switch_player(self, switch):
        # 点击菜单
        await self._click_xy(switch[1] + 20, switch[2] + 20)
        self._free()

    @idle
    @asyncthrows
    async def switch_find_player(self, player, callback):
        target = 'players/' + player
        top_left = self._archor_low_precision(target)
        if top_left:
            await self._player_switch(target)
            callback(player)
            self._free()
            return
        print('【选择角色】当前页没找到，翻到下页')
        await self._player_switch_next()
        await asyncio.sleep(1.5)
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
    async def back_town_mission(self, reset):
        reset()
        top_left = self._archor('close')
        if top_left:
            await self._click('close')

        top_left = self._archor('back')
        if top_left:
            await self._click('back')
        self._free()

    @idle
    @asyncthrows
    async def back_town_dungeon(self, reset):
        reset()
        await self._press('F8')
        await asyncio.sleep(5)
        self._free()

    @idle
    @asyncthrows
    async def back_town_daily(self, back=True):
        await self._click('close')
        if back:
            await self._click('back')
        self._free()

    @idle
    @asyncthrows
    async def back_town_union_signed(self):
        top_left = self._archor('close')
        if top_left:
            await self._click('close')
            await self._click('back')

        top_left = self._archor('back')
        if top_left:
            await self._click('back')
        # 等待线程检测到签到已结束
        await asyncio.sleep(5)
        self._free()

    @idle
    @asyncthrows
    async def back_town_coin_received(self):
        top_left = self._archor('back')
        if top_left:
            await self._click('back')
        # 等待线程检测到复活币领取已结束
        await asyncio.sleep(5)
        self._free()

    @idle
    @asyncthrows
    async def back_town_achievement(self):
        top_left = self._archor('back')
        if top_left:
            await self._click('back')
        # 等待线程检测到成就领取已结束
        await asyncio.sleep(5)
        self._free()

    @idle
    @asyncthrows
    async def back_town(self, setting, reset):
        reset()
        await self._click_xy(setting[1], setting[2])
        await self._click('home')
        await self._click_if('confirm', 'confirm_kr')
        await asyncio.sleep(5)
        self._free()

    @idle
    @asyncthrows
    async def heaven_mission_receive(self):
        await self._click_if('heaven_mission_receive', 'heaven_mission_receive_kr')
        print('【探索者】天界任务领取')
        self._free()

    async def _key_hold(self, key, holding=1):
        keyDown(key)
        await asyncio.sleep(holding)
        keyUp(key)

    @idle
    @asyncthrows
    async def out_stuck(self, direction):
        await self._press('x', 0.3)
        await self._key_hold(direction)
        print('【探索者】正在脱困')
        self._free()

    async def _click_low_precision_callback(self, target, callback, sleep=1, img=None):
        top_left = self._archor_low_precision(target, img)
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            await asyncio.sleep(sleep)
            await callback()

    @idle
    @asyncthrows
    async def union_sign_start(self):
        print('【探索者】5s后打开公会界面')
        await self._active_window()
        await self._press("F7")
        # await self.union_box()
        self._free()

    @idle
    @asyncthrows
    async def union_sign(self):
        await self._click('guild_sign')
        await self._click('guild_gold_sign')
        await self._click_if('confirm', 'confirm_kr', 2)
        await self._click_if('confirm', 'confirm_kr', 2)
        self._free()

    @idle
    @asyncthrows
    async def union_box_sign(self, target, target_kr, callback):
        top_left = self._archor_low_precision_if(target, target_kr)
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y - 120)
            await asyncio.sleep(5)
            await self._press('esc')
            callback()

        self._free()

    @idle
    @asyncthrows
    async def goto_mall_recovered_product(self):
        print('【探索者】打开商城界面')
        await self._active_window()
        await asyncio.sleep(2)
        await self._press("F3")
        await self._click_if("mall_prop", "mall_prop_kr")
        await self._click_if("mall_recovered_product", "mall_recovered_product_kr")
        self._free()

    @idle
    @asyncthrows
    async def mall_purchase(self):
        await self._click_if("mall_purchase", "mall_purchase_kr", 2)
        await self._click_if("mall_purchase", "mall_purchase2_kr", 2)
        await self._press('esc')
        self._free()

    def demon_start(self):
        pass

    @idle
    @asyncthrows
    async def repair(self):
        await self._click('disrepair')
        await self._click_if('repair_confirm', 'repair_confirm_kr')
        await self._click('close')
        self._free()

    @idle
    @asyncthrows
    async def goto_achievement(self):
        print('【探索者】5s后打开成就界面')
        await asyncio.sleep(5)
        await self._click('active')
        await self._click('achievement')
        self._free()

    async def _achievement_box(self, targets):
        await asyncio.sleep(1)
        top_left = self._archor(targets.pop())
        if top_left:
            x, y = top_left
            await self._click_xy(x, y - 100, 2)
            await self._press('esc')

    @idle
    @asyncthrows
    async def achievement_daily_box(self):
        print('【成就】领取每日箱子')
        targets = ['achievement_daily_3', 'achievement_daily_6', 'achievement_daily_9']
        self._achievement_box(targets)
        self._free()

    @idle
    @asyncthrows
    async def achievement_get_all(self):
        print('【成就】一键领取')
        await self._click_if('get_all', 'get_all_kr', 3)
        await self._press('esc')
        self._free()

    @idle
    @asyncthrows
    async def achievement_daily_sella(self):
        print('【成就】领取泰拉箱子')
        await self._click('achievement_daily_sella')
        await self._click_if("achievement_sella_box_use", "achievement_sella_box_use_kr", 2)
        await self._press('esc')
        self._free()

    @idle
    @asyncthrows
    async def goto_achievement_weekly(self):
        print('【成就】转到每周福利')
        await self._click_if('achievement_daily_dis', 'achievement_daily_dis_kr')
        self._free()

    @idle
    @asyncthrows
    async def achievement_weekly_box(self):
        print('【成就】领取每周箱子')
        targets = ['achievement_weekly_2', 'achievement_weekly_4', 'achievement_weekly_6', 'achievement_weekly_8',
                   'achievement_weekly_10']
        await self._achievement_box(targets)
        self._free()

    @idle
    @asyncthrows
    async def goto_mail(self):
        print('【福利】正在打开邮件')
        await self._click('mail')
        self._free()

    @idle
    @asyncthrows
    async def mail_self(self):
        await self._click_if('mail_self', 'mail_self_kr')
        self._free()

    @idle
    @asyncthrows
    async def mail_receive(self):
        await self._click_if('mail_receive', 'mail_receive_kr')
        await self._click_if('confirm', 'confirm_kr')
        await self._click_if('mail_del', 'mail_del_kr')
        self._free()

    @idle
    @asyncthrows
    async def goto_vault(self, bag):
        await self._click_xy(bag[1] + 10, bag[2] + 8)
        await self._click_if('collect_vault', 'collect_vault_kr')
        await self._click_if('collect_gang_vault', 'collect_gang_vault_kr')
        self._free()

    @idle
    @asyncthrows
    async def click_any(self, target):
        await self._click(target)
        self._free()

    @idle
    @asyncthrows
    async def precious_to_vault(self, preciouses, callback):
        img = capture(640, 0, 640, 800)
        click_count = 0
        for item in preciouses:

            top_left = self._archor_best(f"preciouses/{item['target']}", img)
            if top_left:
                x, y = top_left
                await self._click_xy(640 + x + 15, y + 15, 0.5)
                item['collect'] = 2 if 'target_binding' not in item else 1
                click_count += 1

            if 'target_binding' in item:
                top_left = self._archor(f"preciouses/{item['target_binding']}", img)
                if top_left:
                    x, y = top_left
                    await self._click_xy(640 + x + 15, y + 15, 0.5)
                    item['collect'] = 2 if item['collect'] == 1 else 1
                    click_count += 1

        if click_count > 0:
            await self._click('move_to_vault')
            await self._click_if('confirm', 'confirm_kr')

        callback()
        self._free()

    @idle
    @asyncthrows
    async def back_town_vault(self):
        top_left = self._archor('close')
        if top_left:
            await self._click('close')

        top_left = self._archor('back')
        if top_left:
            await self._click('back')
        self._free()

    @idle
    @asyncthrows
    async def goto_duel(self):
        print('【探索者】即将打开角斗场')
        await self._active_window()
        await self._press('f4')
        await self._click('duel_ai_fight')
        self._free()

    async def _active_window(self):
        top_left = self._archor('mail')
        if top_left:
            x, y = top_left
            self._click_xy(x - 200, y)

    @idle
    @asyncthrows
    async def duel_ai_fight(self):
        print('【探索者】即将打开角斗场')
        await self._click('duel_ai_fight')
        self._free()

    @idle
    @asyncthrows
    async def duel_challenge(self):
        await self._click_if('duel_challenge', 'duel_challenge_kr')
        await self._click_if('duel_evolution', 'duel_evolution_kr')
        self._free()

    @idle
    @asyncthrows
    async def duel_reward(self):
        await self._click('duel_reward')
        self._free()

    @idle
    @asyncthrows
    async def duel_get_all(self):
        await self._click_if('duel_get_all', 'duel_get_all_kr')
        await self._press('esc')
        self._free()

    @idle
    @asyncthrows
    async def duel_box_sign(self, box, callback):
        top_left = self._archor(box['target'])
        if top_left:
            x, y = top_left
            await self._click_xy(x + 5, y - 20)
            await self._press('esc')
            callback()
        self._free()

    @idle
    @asyncthrows
    async def duel_week(self):
        await self._click_if('duel_week', 'duel_week_kr')
        self._free()

    @idle
    @asyncthrows
    async def duel_season_over(self):
        await self._click_if('duel_season_over', 'duel_season_over_kr')
        self._free()

    @idle
    @asyncthrows
    async def duel_skill_set(self):
        await self._click_if('duel_skill_recommend', 'duel_skill_recommend_kr')
        top_left = self._archor_if('duel_skill_recommend_active', 'duel_skill_recommend_active_kr')
        if top_left:
            await self._click_if('duel_skill_use', 'duel_skill_use_kr')
            await self._click_if('confirm', 'confirm_kr', 0.5)
            await self._click_if('confirm2', 'confirm2_kr', 0.5)
            await self._click('close2')
        self._free()

    @idle
    @asyncthrows
    async def duel_promotion(self):
        await self._click_if('duel_promotion', 'duel_promotion_kr')
        self._free()

    @idle
    @asyncthrows
    async def back_home(self, reset):
        reset()
        await self._click('home')
        await self._click_if('confirm', 'confirm_kr')
        await asyncio.sleep(5)
        self._free()

    @idle
    @asyncthrows
    async def goto_consumable(self):
        await self._click('consumable')
        self._free()

    @idle
    @asyncthrows
    async def csb_use(self):
        await self._click_if('csb_use', 'csb_use_kr')
        self._free()

    @idle
    @asyncthrows
    async def csb_onekey(self):
        await self._click_if('csb_onekey', 'csb_onekey_kr')
        self._free()

    @idle
    @asyncthrows
    async def csb_use_large(self):
        await self._click_if('csb_use_large_kr', 'csb_use_large_kr')
        self._free()

    @idle
    @asyncthrows
    async def back_share(self):
        await self._click_if('back_share', 'back_share_kr')
        self._free()

    @idle
    @asyncthrows
    async def daily_stage_change(self, stage):
        await self._click_if(f'daily_stage_{stage}', f'daily_stage_{stage}_kr')
        self._free()

    @idle
    @asyncthrows
    async def duel_refresh(self):
        await self._click('duel_refresh')
        self._free()

    @idle
    @asyncthrows
    async def goto_pet(self):
        await self._open_menu()
        await asyncio.sleep(1)
        await self._click('pet')
        self._free()

    @idle
    @asyncthrows
    async def goto_pet_gear(self):
        await self._click_if('pet_gear', 'pet_gear_kr')
        self._free()

    @idle
    @asyncthrows
    async def pet_decompose(self):
        await self._click('pet_decompose')
        self._free()

    @idle
    @asyncthrows
    async def pet_decompose_btn(self):
        await self._click_if('pet_decompose_btn', 'pet_decompose_btn_kr')
        self._free()

    @idle
    @asyncthrows
    async def goto_ms(self):
        await self._open_menu()
        await asyncio.sleep(1)
        await self._click('mystery_store')
        self._free()

    @idle
    @asyncthrows
    async def ms_check_commodity(self, result, callback):
        for x, y in result:
            await self._click_xy(x, y, 0.8)
        callback()
        self._free()

    @idle
    @asyncthrows
    async def purchase(self):
        await self._click_if("mall_purchase", "mall_purchase_kr", 2)
        self._free()
