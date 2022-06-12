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
        self.lion_entry_stand_count = 0

    def init(self):
        self.running = True

    def meeting_lion(self):
        self.is_meeting_lion = True
        self.lion_entry_stand_count = 0

    def _run(self):
        cls = self.voyager.recogbot.detect()

        # 发现狮子头入口
        if self.voyager.game.lionAlive and cls['door'][0] and cls['lion_entry'][0]:
            print("【雪山战斗】发现狮子头入口!", self.voyager.game.lionAlive)
            self.is_meeting_lion = False
            if self.lion_entry_stand_count < 1:
                self.voyager.player.stand()
            # 卡住自救
            if self.lion_entry_stand_count > 100:
                self.voyager.player.stop_right()
                self.voyager.player.dodge_direction('left')
                self.lion_entry_stand_count = 1

            self.lion_entry_stand_count += 1
            self.voyager.player.right()

        # 狮子头入口，门没开，修改战斗方式
        if self.voyager.game.lionAlive and not cls['door'][0] and cls['lion_entry'][0]:
            # 已接触敌人，停止原战斗方式
            if cls['combo'][0]:
                self.voyager.player.stand()
                self.voyager.player.slowly_hit()
            else:
                self.voyager.player.attack_active()

        if not cls['lion_entry'][0]:
            self.voyager.player.attack_active()

        # 出现对话时按Esc跳过
        if cls['skip'][0] or self.voyager.recogbot.talk_skip():
            self.voyager.game.esc()

        # 释放技能
        if (cls['combo'][0] and cls['avatar'][0]) or (cls['combo'][0] and cls['boss'][0]):
            print("【雪山战斗】还有小可爱活着")
            self.voyager.player.cast()
            self.voyager.matric.combo(cls['combo'])

        # 释放觉醒
        if cls['boss'][0]:
            print("【雪山战斗】发现Boss!")
            self._finisher()

        if cls['demon'][0]:
            print("【雪山战斗】发现深渊恶魔!")
            self._finisher()

        # 狮子头
        if cls['lion'][0]:
            print("【雪山战斗】发现狮子头!")
            if not self.is_meeting_lion:
                self.voyager.player.attack_active()
                self.voyager.player.stop_right()
                self.meeting_lion()

            self.voyager.game.lion_clear()
            self.voyager.player.attack()
            self._finisher()

    def _finisher(self):
        if self.voyager.recogbot.skill(self.voyager.player.awake['icon']):
            self.voyager.player.finisher()

    def run(self):
        self.init()
        print("【雪山战斗】战斗开始执行")
        while self.running:
            self._run()

    def stop(self):
        print("【雪山战斗】战斗停止执行")
        self.running = False
