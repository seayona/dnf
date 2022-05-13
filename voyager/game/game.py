from PyQt5.QtCore import QTimer

from voyager.control import moveTo, click, press
from voyager.recognition import capture, match, Recogbot


class Game(object):
    def __init__(self):
        self.freezy = True
        self.repaired = False
        self.recogbot = Recogbot()
        self.timer = QTimer()

    def _archor(self, target):
        # 获取屏幕截图
        img = capture()
        # 检测再次挑战的按钮位置
        max_val, img, top_left, right_bottom = match(img, './game/scene/' + target + '.png')
        if 1 >= max_val > 0.99:
            # 返回按钮位置
            x, y = top_left
            return x + 10, y + 8

    def _click(self, target):
        top_left = self._archor(target)
        if top_left:
            x, y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)

    def _free(self):
        self.freezy = True

    def replay(self):
        if self.freezy:
            self.freezy = False
            self.repaired = False
            self._click('replay')
            self.timer.singleShot(1000, lambda: self._click('confirm'))
            self.timer.singleShot(1200, lambda: self._free())
            self.timer.singleShot(1200, lambda: print('【探索者】开始再次挑战'))

    def reward(self):
        if self.freezy:
            self.freezy = False
            self._click('gold')
            self.timer.singleShot(1000, lambda: self._click('gold2'))
            self.timer.singleShot(2200, self._free('【探索者】奖励领取成功'))

    def repair(self):
        if self.repaired:
            print("【探索者】已修理，无需修理")
            return
        if self.freezy and not self.repaired:
            self.freezy = False
            # 打开背包
            self._click('bag')
            # 点击分解按钮
            self.timer.singleShot(1000, lambda: self._click('repair'))
            # 确认分解
            self.timer.singleShot(2000, lambda: self._click('repair_confirm'))
            # 返回！
            self.timer.singleShot(3000, lambda: press('esc'))
            # 返回！!
            self.timer.singleShot(4000, lambda: press('esc'))
            # 返回！!
            self.timer.singleShot(4500, lambda: press('esc'))
            # 返回！!
            self.timer.singleShot(4600, self._onrepaired)
            # 返回！!
            self.timer.singleShot(4600, self._free)

    def _onrepaired(self):
        self.repaired = True
        print('【探索者】装备修理完成')
