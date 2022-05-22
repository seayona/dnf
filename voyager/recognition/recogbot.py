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
                if names[int(cls)] == 'monster' and float(f'{conf:.2f}') > 0.5:
                    return True
                if names[int(cls)] == 'tiger' and float(f'{conf:.2f}') > 0.5:
                    return True
                if names[int(cls)] == 'ice' and float(f'{conf:.2f}') > 0.5:
                    return True
                if names[int(cls)] == 'boss_label' and float(f'{conf:.2f}') > 0.5:
                    return True
                if names[int(cls)] == 'lion' and float(f'{conf:.2f}') > 0.5:
                    return True
                if names[int(cls)] == 'door' and float(f'{conf:.2f}') > 0.8:
                    return False
        return False

    def detect(self):
        pred, names = detect()
        monster = lion = boss = door = False
        for i, det in enumerate(pred):
            if len(det) < 1:
                continue
            for *_, conf, cls in reversed(det):
                if names[int(cls)] == 'monster' and float(f'{conf:.2f}') > 0.5:
                    monster = True
                if names[int(cls)] == 'tiger' and float(f'{conf:.2f}') > 0.5:
                    monster = True
                if names[int(cls)] == 'ice' and float(f'{conf:.2f}') > 0.5:
                    monster = True
                if names[int(cls)] == 'boss_label' and float(f'{conf:.2f}') > 0.8:
                    boss = True
                if names[int(cls)] == 'lion' and float(f'{conf:.2f}') > 0.5:
                    monster = True
                    lion = True
                if names[int(cls)] == 'door' and float(f'{conf:.2f}') > 0.8:
                    door = True
                    monster = False
                    lion = False
                    boss = False
        return monster, lion, boss, door

    def lion(self):
        pred, names = detect()
        for i, det in enumerate(pred):
            if len(det) < 1:
                continue
            for *_, conf, cls in reversed(det):
                if names[int(cls)] == 'lion' and float(f'{conf:.2f}') > 0.6:
                    return True
        return False

    def door(self):
        pred, names = detect()
        for i, det in enumerate(pred):
            if len(det) < 1:
                continue
            for *_, conf, cls in reversed(det):
                if names[int(cls)] == 'monster' and float(f'{conf:.2f}') > 0.5:
                    return False
                if names[int(cls)] == 'tiger' and float(f'{conf:.2f}') > 0.5:
                    return False
                if names[int(cls)] == 'door' and float(f'{conf:.2f}') > 0.8:
                    return True
        return False

    def reward(self):
        return self._recog('reward')

    def replay(self):
        return self._recog('replay') or self._recog('replay_kr')

    def demon(self):
        pass

    def disrepair(self):
        pass

    def clear(self):
        return self._recog('go')

    def boss(self):
        return self._recog('boss')

    def boss_valley(self):
        return self._recog('valley_boss')

    def bag(self):
        return self._recog('bag')

    def result(self):
        return self._recog('result')

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

    def talk(self):
        img = capture(1100, 0, 150, 150)
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, f'./game/scene/talk_skip.png')
        # print(f'【模板匹配】 {target} {max_val}')
        if 0.94 < max_val <= 1:
            return True
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, f'./game/scene/talk_skip_kr.png')
        return 0.94 < max_val <= 1

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
        return self._recog('jump')

    def combo(self):
        return self._recog_low_precision('combo')
