
from detect_dnf import detect
from voyager.recognition import capture, match


class Recogbot(object):

    def __init__(self):
        pass

    def _recog(self, target):
        # 获取屏幕截图
        img = capture()
        # 检测目标位置
        max_val, img, top_left, right_bottom = match(img, './game/scene/' + target + '.png')
        # print(f'【模板匹配】 {target} {max_val}')
        return 0.99 < max_val <= 1

    def loveyAlive(self):
        pred, names = detect()
        for i, det in enumerate(pred):
            if len(det) < 1:
                continue
            for *_, conf, cls in reversed(det):
                if names[int(cls)] == 'monster' and float(f'{conf:.2f}') > 0.8:
                    return True
                if names[int(cls)] == 'tiger' and float(f'{conf:.2f}') > 0.7:
                    return True
                if names[int(cls)] == 'ice' and float(f'{conf:.2f}') > 0.7:
                    return True
                if names[int(cls)] == 'door' and float(f'{conf:.2f}') > 0.7:
                    return False
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

    def map(self):
        if self._recog('m1'):
            return 1
        if self._recog('m2'):
            return 2
        if self._recog('m3'):
            return 3
        if self._recog('m4'):
            return 4
        if self._recog('m5'):
            return 5
        if self._recog('m6'):
            return 6
        if self._recog('m7'):
            return 7
        if self._recog('me') or self._recog('mr'):
            return 9
        return 0

    def boss(self):
        return self._recog('boss')

    def boss_valley(self):
        return self._recog('valley_boss')

    def bag(self):
        return self._recog('bag')

    def result(self):
        return self._recog('result')

    def lion(self):
        return self._recog('lion')

    def door(self):
        pred, names = detect()
        for i, det in enumerate(pred):
            if len(det) < 1:
                continue
            for *_, conf, cls in reversed(det):
                if names[int(cls)] == 'monster' and float(f'{conf:.2f}') > 0.85:
                    return False
                if names[int(cls)] == 'tiger' and float(f'{conf:.2f}') > 0.5:
                    return False
                if names[int(cls)] == 'door' and float(f'{conf:.2f}') > 0.5:
                    return True
        return True

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
