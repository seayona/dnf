from detect_dnf import detect
from voyager.recognition import capture, match

class Recogbot(object):

    def __init__(self):
        pass

    def _recog(self, target):
        # 获取屏幕截图
        img = capture()
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, f'./game/scene/{target}.png')
        # print(f'【模板匹配】 {target} {max_val}')
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
        return self._recog('replay')

    def demon(self):
        pass

    def disrepair(self):
        pass

    def clear(self):
        return self._recog('go')

    # def map(self):
    #     if self._recog('m1'):
    #         return 1
    #     if self._recog('m2'):
    #         return 2
    #     if self._recog('m3'):
    #         return 3
    #     if self._recog('m4'):
    #         return 4
    #     if self._recog('m5'):
    #         return 5
    #     if self._recog('m6'):
    #         return 6
    #     if self._recog('m7'):
    #         return 7
    #     if self._recog('me') or self._recog('mr'):
    #         return 9
    #     return 0

    def boss(self):
        pred, names = detect()
        for i, det in enumerate(pred):
            if len(det) < 1:
                continue
            for *_, conf, cls in reversed(det):
                if names[int(cls)] == 'boss_label' and float(f'{conf:.2f}') > 0.8:
                    return True
        return False

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
        return self._recog('valley_town')

    def entry_snow_mountain(self):
        return self._recog('adventure_snow_mountain_entry')

    def dead(self):
        return self._recog('dead')

    def insufficient_balance(self):
        return self._recog('insufficient_balance')

    def lion_clear(self):
        return self._recog('lion_clear')

    def talk(self):
        return self._recog('talk_skip')

    def confirm(self):
        return self._recog('confirm')

    def setting(self):
        return self._recog('setting')

    def next(self):
        return self._recog('next')

    def next_agency(self):
        return self._recog('next_agency')

    def next_agency_confirm(self):
        return self._recog('next_agency_confirm')

    def equip(self):
        return self._recog('equip')

    def click_close(self):
        return self._recog('click_close')

    def back(self):
        return self._recog('back')

    def lion_entry2(self):
        # 获取屏幕截图
        img = capture()
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, f'./game/scene/lion_entry.png')
        # print(f'【模板匹配】 lion_entry {max_val}')
        return 0.94 < max_val <= 1

    def lion_entry1(self):
        # 获取屏幕截图
        img = capture()
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, f'./game/scene/lion_entry2.png')
        # print(f'【模板匹配】 lion_entry {max_val}')
        return 0.94 < max_val <= 1

    def lion_entry(self):
        # 获取屏幕截图
        img = capture()
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, f'./game/scene/lion.png')
        # print(f'【模板匹配】 lion {max_val}')
        return 0.94 < max_val <= 1

    def insufficient_balance_demon(self):
        # 获取屏幕截图
        img = capture()
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, f'./game/scene/insufficient_balance_demon.png')
        # print(f'【模板匹配】 lion {max_val}')
        return 0.94 < max_val <= 1


