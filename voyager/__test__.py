import asyncio
import threading
import time

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from recognition import match, capture

if __name__ == '__main__':
    while True:
        result = match(capture(), './game/scene/menu.png', True)
        print(result[0])