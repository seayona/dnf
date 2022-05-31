from detect_dnf import detect
from voyager.recognition import capture, match


class Recogbot(object):

    def __init__(self):
        pass

    def _match_max_val(self, target):
        # 获取屏幕截图
        img = capture()
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, f'./game/scene/{target}.png')
        # print(f'【模板匹配】 {target} {max_val}')
        return max_val

    def _recog(self, target):
        return 0.99 < self._match_max_val(target) <= 1

    def _recog_if(self, target1, target2):
        max_val = self._match_max_val(target1)
        if 0.99 < max_val <= 1:
            return True
        max_val = self._match_max_val(target2)
        return 0.99 < max_val <= 1

    def _recog_low_precision(self, target):
        max_val = self._match_max_val(target)
        return 0.94 < max_val <= 1

    def _recog_low_precision_if(self, target, target2):
        max_val = self._match_max_val(target)
        if 0.94 < max_val <= 1:
            return True
        max_val = self._match_max_val(target2)
        return 0.99 < max_val <= 1

    def loveyAlive(self):
        pred, names = detect()
        for i, det in enumerate(pred):
            if len(det) < 1:
                continue
            for *_, conf, cls in reversed(det):
                if names[int(cls)] == 'avatar' and float(f'{conf:.2f}') > 0.5:
                    return True
                if names[int(cls)] == 'lion' and float(f'{conf:.2f}') > 0.5:
                    return True
                if names[int(cls)] == 'boss' and float(f'{conf:.2f}') > 0.5:
                    return True
                if names[int(cls)] == 'next' and float(f'{conf:.2f}') > 0.5:
                    return False
                if names[int(cls)] == 'door' and float(f'{conf:.2f}') > 0.5:
                    return False
        return False

    def detect(self):
        pred, names = detect()
        result = {}
        for s in ['lion', 'boss', 'avatar', 'next', 'bag', 'tutorial', 'skip', 'lion_entry', 'combo', 'door']:
            result[s] = (False, 0, 0)
        for i, det in enumerate(pred):
            if len(det) < 1:
                continue
            for *xyxy, conf, cls in reversed(det):
                x, y = (int(xyxy[0]) * 2, int(xyxy[1]) * 2)
                if names[int(cls)] == 'avatar' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到小可爱")
                    result['avatar'] = (True, x, y)
                if names[int(cls)] == 'skip' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到动画")
                    result['skip'] = (True, x, y)
                if names[int(cls)] == 'boss' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到大Boss")
                    result['boss'] = (True, x, y)
                if names[int(cls)] == 'lion' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到狮子头")
                    result['lion'] = (True, x, y)
                if names[int(cls)] == 'lion_entry' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到狮子头入口", (x, y))
                    result['lion_entry'] = (True, x, y)
                if names[int(cls)] == 'bag' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到背包", (x, y))
                    result['bag'] = (True, x, y)
                if names[int(cls)] == 'next' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到下个任务", (x, y))
                    result['next'] = (True, x, y)
                if names[int(cls)] == 'tutorial' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】检测到游戏教程", (x, y))
                    result['tutorial'] = (True, x, y)
                if names[int(cls)] == 'combo' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】连击数", (x, y))
                    result['combo'] = (True, x, y)
                if names[int(cls)] == 'door' and float(f'{conf:.2f}') > 0.5:
                    print("【实时检测】连击数", (x, y))
                    result['door'] = (True, x, y)
        return result

    def lion(self):
        pred, names = detect()
        for i, det in enumerate(pred):
            if len(det) < 1:
                continue
            for *_, conf, cls in reversed(det):
                if names[int(cls)] == 'lion' and float(f'{conf:.2f}') > 0.6:
                    return True
        return False

    def reward(self):
        return self._recog('reward')

    def replay(self):
        return self._recog_low_precision_if('replay', 'replay_kr')

    def clear(self):
        return self._recog('go')

    def boss(self):
        return self._recog('boss')

    def boss_valley(self):
        return self._recog('valley_boss')

    def bag(self):
        return self._recog('bag')

    def result(self):
        return self._recog_low_precision('result')

    def active(self):
        return self._recog('active')

    def daily(self):
        return self._recog('daily')

    def daily_valley(self):
        return self._recog('valley')

    def daliy_valley_completed(self):
        return self._recog('valley_completed')

    def daily_valley_town(self):
        return self._recog_if('valley_town', 'valley_town_kr')

    def entry_snow_mountain(self):
        return self._recog('adventure_snow_mountain_entry')

    def dead(self):
        return self._recog_if('dead', 'dead_kr')

    def insufficient_balance(self):
        return self._recog_low_precision_if('insufficient_balance', 'insufficient_balance_kr')

    def lion_clear(self):
        return self._recog('lion_clear')

    def detect_skip(self):
        pred, names = detect()
        skip = False
        for i, det in enumerate(pred):
            if len(det) < 1:
                continue
            for *xyxy, conf, cls in reversed(det):
                x, y = (int(xyxy[0]), int(xyxy[1]))
                if names[int(cls)] == 'skip' and float(f'{conf:.2f}') > 0.8:
                    skip = True
                    print("检测到对话", (x, y))
                if names[int(cls)] == 'tutorial' and float(f'{conf:.2f}') > 0.6:
                    skip = True
                    print("【目标检测】检测到教程", (x, y))
        return skip

    def confirm(self):
        return self._recog_if('confirm', 'confirm_kr')

    def setting(self):
        return self._recog('setting')

    def next(self):
        img = capture(990, 0, 300, 380)
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, f'./game/scene/next.png')
        # print(f'【模板匹配】 {target} {max_val}')
        return 0.94 < max_val <= 1

    def next_agency(self):
        return self._recog('next_agency')

    def next_agency_confirm(self):
        return self._recog('next_agency_confirm')

    def equip(self):
        return self._recog_if('equip', 'equip_kr')

    def click_close(self):
        return self._recog_low_precision('click_close')

    def back(self):
        return self._recog('back')

    def lion_entry2(self):
        return self._recog_low_precision('lion_entry')

    def lion_entry1(self):
        return self._recog_low_precision('lion_entry2')

    def lion_entry(self):
        return self._recog_low_precision('lion')

    def insufficient_balance_demon(self):
        return self._recog_low_precision_if('insufficient_balance_demon', 'insufficient_balance_demon_kr')

    def sylia(self):
        return self._recog_if('sylia', 'sylia_kr')

    def insufficient_balance_mission(self):
        return self._recog_low_precision('insufficient_balance_mission')

    def agency_mission_confirm(self):
        return self._recog_if('agency_mission_confirm', 'agency_mission_confirm_kr')

    def next_agency_none(self):
        return self._recog('next_none')

    def agency_mission_get(self):
        return self._recog_if('agency_mission_get', 'agency_mission_get_kr')

    def town(self):
        return self._recog('mail')

    def message(self):
        return self._recog('message')

    def attack(self):
        return self._recog('attack')

    def jump(self):
        return self._recog_low_precision('jump')

    def combo(self):
        return self._recog_low_precision('combo')

    def buff(self, target):
        return self._recog_low_precision('skills/' + target)

    def close(self):
        return self._recog('close')

    def back_to_town(self):
        return self._recog_if('adventure_snow_mountain_town', 'adventure_snow_mountain_town_kr')

    def heaven_mission_receive(self):
        return self._recog_if('heaven_mission_receive', 'heaven_mission_receive_kr')

    def _recog_cheap(self, target):
        max_val = self._match_max_val(target)
        return 0.9 < max_val <= 1

    def black_town_stuck(self):
        return self._recog_cheap('black_town_stuck')

    def heaven_stuck(self):
        return self._recog_low_precision_if('heaven_stuck1', 'heaven_stuck2')

    def _recog_diy_precision(self, target, low, height=1):
        max_val = self._match_max_val(target)
        return low <= max_val <= height

    def talk_skip(self):
        return self._recog_low_precision_if('talk_skip_kr', 'talk_skip')

    def union_sign(self):
        return self._recog('guild_sign')

    def union_box1_signed(self):
        return self._recog_diy_precision('guild_signed_coin', 0.97)

    def union_box2_signed(self):
        return self._recog_diy_precision('guild_signed_pill', 0.97)

    def union_box3_signed(self):
        return self._recog_diy_precision('guild_signed_carbon', 0.97)

    def union_box4_signed(self):
        return self._recog_diy_precision('guild_signed_book', 0.97)

    def union_box_signed(self, index):
        fun_name = "union_box{}_signed".format(index + 1)
        fun = getattr(self, fun_name)
        return fun()

    def revival_coin_received(self):
        return self._recog_if('mall_coin_received', "mall_coin_received_kr")

    def revival_coin_status(self):
        return self._recog("mall_price") and self._recog_if("mall_purchase", "mall_purchase_kr")
