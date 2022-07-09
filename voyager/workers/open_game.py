import win32gui
from PyQt5.QtCore import QThread, pyqtSignal


class OpenGame(QThread):
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        self.running = False

    def init(self):
        self.running = True

    def _run(self):
        # 时间检测
        # 打开加速器
        # 一键加速
        # 打开游戏
        # 开启游戏
        # 移动游戏窗口
        # 关闭各种游戏弹窗
        # 开启搬砖线程
        pass

    def _move_game_window(self):
        hwd = win32gui.FindWindow(0, '游戏窗口名')
        rect = win32gui.GetWindowRect(hwd)
        w = rect[2] - rect[0]
        h = rect[3] - rect[1]
        win32gui.MoveWindow(hwd, 0, 0, w, h, True)

    def run(self) -> None:
        self.init()
        while self.running:
            self._run()
