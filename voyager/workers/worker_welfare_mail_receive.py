import time

from PyQt5.QtCore import QThread, pyqtSignal
from .woker_pet_gear import PetGear


class WelfareMailReceive(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        super(WelfareMailReceive, self).__init__()
        self.voyager = voyager
        self.running = False
        self.in_pet_clear = False
        self.pet_cleared = False
        self.p = None

    def init(self):
        self.p = None
        self.running = True
        self.pet_cleared = False
        self.in_pet_clear = False

    def _run(self):
        if self.in_pet_clear:
            return
        if self.voyager.recogbot.town() and self.voyager.player.welfare['mail']:
            self.voyager.matric.heartbeat()
            self.trigger.emit(self.__class__.__name__)

        if self.voyager.recogbot.town() and not self.voyager.player.welfare['mail']:
            self.voyager.game.goto_mail()

        if self.voyager.recogbot.mail_self():
            self.voyager.game.mail_self()

        if self.voyager.recogbot.mail_receive() and self.voyager.recogbot.mail_self_active():
            self.voyager.game.mail_receive()

        if self.voyager.recogbot.mail_received() and self.voyager.recogbot.mail_self_active():
            self.voyager.matric.heartbeat()
            self.voyager.player.over_welfare('mail')
            self.voyager.game.back()

        # 宠物装备溢出，开启宠物装备分解线程
        if self.voyager.recogbot.mail_self_active() and self.voyager.recogbot.mail_overflow_pet_gear() and not self.pet_cleared:
            self.in_pet_clear = True
            self._open_pet_thread()

    def _open_pet_thead(self):
        if self.p is not None:
            return
        self.p = PetGear(self.voyager)
        self.p.trigger.connect(self.pet_finish)

    def pet_finish(self):
        self.in_pet_clear = True
        self.pet_cleared = True
        self.p.stop()
        self.p = None

    def run(self):
        self.init()
        print("【自动福利】邮件开始执行")
        while self.running:
            self._run()
            self.sleep(1)

    def stop(self):
        print("【自动福利】复活币福利执行结束")
        self.running = False
