import asyncio
import threading
import time

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from infrastructure import Notification, Matric
from recognition import match, capture, match_best, match_all_best

if __name__ == '__main__':
    m = Matric()
    for i in range(10):
        m.heartbeat()
        time.sleep(1)
