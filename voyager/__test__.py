import asyncio
import time

import cv2
import numpy as np

from voyager.game import Player, Skill, Game
from voyager.infrastructure import Notification, Concurrency, idle, asyncthrows
from voyager.recognition import Recogbot, capture, match


class A(Concurrency):

    def __init__(self):
        super().__init__()

    @idle
    async def foo(self):
        b = B()
        print("foo -> bar")
        await b.bar()


class B(Concurrency):
    def __init__(self):
        super().__init__()

    @asyncthrows
    async def bar(self):
        print("bar -> sleep(1)")
        await asyncio.sleep(1)
        raise Exception('aaa')


if __name__ == '__main__':
    # while True:
    #     # 获取屏幕截图
    #     img = capture()
    #     tmp = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     _, alpha = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
    #     b, g, r = cv2.split(img)
    #     rgba = [b, g, r, alpha]
    #     dst = cv2.merge(rgba, 4)
    #     # 检测目标位置
    #     max_val, img, top_left, right_bottom = match(img, f'./game/scene/result.png', True)
    #     print(f'【模板匹配】 next {max_val}')

    # notification = Notification()
    # notification.send('【Tyrrell】疲劳已耗尽')

    # player = Player('Seayona')
    # player.cast('E-2-Y-1-B')
    # player.cast('Q')
    # player.cast('O')
    # player.cast('U')

    player = Player('Tyrrell')
    recogbot = Recogbot()

    while True:
        for key in player.buff.keys():
            if recogbot.buff(key):
                player.release_buff(key)
