import cv2
import numpy as np

from voyager.infrastructure import Notification
from voyager.recognition import Recogbot, capture, match

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

    notification = Notification()
    notification.send('【Tyrrell】疲劳已耗尽')