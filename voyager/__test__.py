import asyncio
import threading
import time

import cv2
import numpy as np
from PyQt5.QtCore import QThread, pyqtSignal

from voyager.game import Player, Skill, Game
from voyager.infrastructure import Notification, Concurrency, idle, asyncthrows
from voyager.recognition import Recogbot, capture, match


class Base(QThread):
    trigger = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.b = B()
        self.running = True

    def run(self):
        self.b.start()
        while self.running:
            print("【探索者】线程A正在运行ID", int(QThread.currentThreadId()))
            time.sleep(1)

    def stop(self):
        self.b.stop()
        self.running = False
        print("【探索者】线程B停止", int(QThread.currentThreadId()))

class A(QThread):
    trigger = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.b = B()
        self.running = True

    def run(self):
        self.b.start()
        self.running = True
        while self.running:
            print("【探索者】线程A正在运行ID", int(QThread.currentThreadId()))
            time.sleep(1)

    def stop(self):
        self.b.stop()
        self.running = False
        print("【探索者】线程B停止", int(QThread.currentThreadId()))


class B(QThread):
    trigger = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.c = C()
        self.running = True

    def run(self):
        count = 0
        while self.running:
            if count == 5:
                self.c.start()
            if count == 10:
                self.c.stop()
                print("【探索者】线程C停止", int(QThread.currentThreadId()))
                self.trigger.emit(str('stop'))
            count = count + 1
            print("【探索者】线程B正在运行ID", int(QThread.currentThreadId()))
            time.sleep(1)

    def stop(self):
        self.c.stop()
        self.running = False


class C(QThread):
    def __init__(self):
        super().__init__()
        self.running = True
    def run(self):
        while self.running:
            print("【探索者】线程C正在运行ID", int(QThread.currentThreadId()))
            time.sleep(1)

    def stop(self):
        self.running = False


if __name__ == '__main__':
    seed = 1
    a = A()
    a.start()
    while True:
        print('threading.enumerate()', threading.enumerate())
        print("threading.active_count()", threading.active_count())
        print("a.isRunning()", a.isRunning())
        print("a.isFinished()", a.isFinished())
        print("【探索者】线程main正在运行ID", int(QThread.currentThreadId()))
        seed = seed + 1
        if seed == 10:
            a.stop()
            print("【探索者】线程A停止", int(QThread.currentThreadId()))
        if seed > 20:
            a.start()
            print('a.running', a.running)
        time.sleep(2)
