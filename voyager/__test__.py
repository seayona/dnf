import asyncio
import threading
import time

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from recognition import match, capture

if __name__ == '__main__':
    while True:
        result = match(capture(640, 0, 640, 800), './game/scene/empty_cell.PNG', True)
        print(result[0], result[2])
