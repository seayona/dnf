import time

from PyQt5.QtCore import QThread, pyqtSignal


class PetGear(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareMailReceive, self).__init__()
        self.voyager = voyager
        self.running = False
        self.clear = False

    def init(self):
        self.running = True
        self.clear = False

    def _run(self):
        if self.voyager.recogbot.town() and not self.clear:
            self.voyager.game.goto_pet()

        # 任务完成，一路esc
        if self.clear and not self.voyager.recogbot.town():
            self.voyager.game.esc()

        if self.clear and self.voyager.recogbot.town():
            self.voyager.matric.heartbeat()
            self.trigger.emit(self.__class__.__name__)

        # 确认按钮
        if self.voyager.recogbot.confirm():
            self.voyager.matric.heartbeat()
            self.voyager.game.confirm()

        # 转到装备
        if self.voyager.recogbot.pet_gear():
            self.voyager.game.goto_pet_gear()

        # 开始分解
        if self.voyager.recogbot.pet_gear_active():
            self.voyager.game.pet_decompose()

        # 分解按钮
        if self.voyager.recogbot.pet_decompose_btn():
            self.voyager.game.pet_decompose_btn()

        # 分解完毕
        if self.voyager.recogbot.pet_lot_empty() and self.voyager.recogbot.pet_in_decompose():
            self.clear = True

    def run(self):
        self.init()
        print("【清理宠物装备】开始执行")
        while self.running:
            self._run()
            self.sleep(1)

    def stop(self):
        print("【清理宠物装备】执行结束")
        self.running = False
