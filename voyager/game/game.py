
from PyQt5.QtCore import QTimer

from voyager.control import moveTo, click
from voyager.recognition import capture, match, Recogbot


class Game(object):
    def __init__(self):
        self.recogbot = Recogbot()
        self.timer = QTimer()

    def _archor(self, target):
        # 获取屏幕截图
        img = capture()
        # 检测再次挑战的按钮位置
        max_val, img, top_left, right_bottom = match(img, './game/scene/' + target + '.png')
        if max_val > 0.99:
            # 返回按钮位置
            x, y = top_left
            return x + 10, y + 8
    def confirm(self):
        top_left = self._archor('confirm')
        if top_left:
            x,y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)

    def replay(self):
        top_left = self._archor('replay')
        if top_left:
            x,y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            # 1秒后点击确认按钮
            self.timer.singleShot(1000, self.confirm)

    def tower(self):
        pass

    def repair(self):
        pass

    def reward(self):
        top_left = self._archor('gold')
        if top_left:
            x,y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            # 1秒后点击确认按钮
            self.timer.singleShot(1000, self.confirm)
        top_left = self._archor('gold2')
        if top_left:
            x,y = top_left
            # 移动鼠标到按钮位置,点击按钮
            click(x, y)
            # 1秒后点击确认按钮
            self.timer.singleShot(1000, self.confirm)