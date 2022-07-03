import asyncio
import threading
import time

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from infrastructure import Notification
from recognition import match, capture, match_best, match_all_best


def _max_all_best(target, img=None):
    img = img if img is not None else capture()
    result = match_all_best(img, target)
    if result is None:
        return None
    res = []
    for item in result:
        if item['confidence'] > 0.99:
            res.append(item['result'])
    if len(res) > 0:
        return res
    else:
        return None


if __name__ == '__main__':
    result = _max_all_best('./game/scene/store/key_fragment.PNG')
    print(result)
    test = [(325, 167), (469, 167), (177, 181), (630, 167)]
    for x, y in test:
        print(x, y)
