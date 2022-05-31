from PyQt5.QtCore import QThread, pyqtSignal


class PlayerFightWorker(QThread):
    # 定义一个信号
    trigger = pyqtSignal(str)

    def __init__(self, voyager):
        # 初始化函数，默认
        super(PlayerFightWorker, self).__init__()
        self.voyager = voyager
        self.running = False
        self.is_meeting_lion = False

    def init(self):
        self.running = True

    def meeting_lion(self):
        self.is_meeting_lion = True

    def _run(self):
        cls = self.voyager.recogbot.detect()

        # 发现狮子头入口
        if self.voyager.game.lionAlive and cls['door'][0] and cls['lion_entry'][0]:
            print("【雪山战斗】发现狮子头入口!", self.voyager.game.lionAlive)
            self.is_meeting_lion = False
            self.voyager.player.stand()
            self.voyager.player.right()

        # 释放技能
        if (cls['combo'][0] and cls['avatar'][0]) or (cls['combo'][0] and cls['boss'][0]):
            print("【雪山战斗】还有小可爱活着")
            self.voyager.player.cast()
            self.voyager.matric.combo(cls['combo'])

        # 释放觉醒
        if cls['boss'][0]:
            print("【雪山战斗】发现Boss!")
            self.voyager.player.finisher()

        # 狮子头
        if cls['lion'][0]:
            print("【雪山战斗】发现狮子头!")
            if not self.is_meeting_lion:
                self.voyager.player.stop_right(lambda: self.meeting_lion())
                
            self.voyager.game.lion_clear()
            self.voyager.player.attack()
            self.voyager.player.finisher()

    def run(self):
        self.init()
        print("【雪山战斗】战斗开始执行")
        while self.running:
            self._run()

    def stop(self):
        print("【雪山战斗】战斗停止执行")
        self.running = False
