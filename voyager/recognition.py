import time

from voyager.game import Game, Player
from voyager.recognition import Recogbot

if __name__ == '__main__':
    recogbot = Recogbot()
    game = Game()
    player = Player()

    while True:
        time.sleep(1)

        if not recogbot.door() and recogbot.setting():
            print(f'【目标检测】检测到下个任务按钮')
            player.cast_random()

        if recogbot.confirm():
            print(f'【目标检测】检测到下个任务按钮')
            game.confirm()

        if recogbot.next():
            print(f'【目标检测】检测到下个任务按钮')
            game.next()

        if recogbot.next_agency():
            print(f'【目标检测】检测到下个主线任务按钮')
            game.next_agency()

        if recogbot.next_agency_confirm():
            print(f'【目标检测】检测到下个主线任务按钮')
            game.next_agency_confirm()

        if recogbot.talk():
            print(f'【目标检测】检测到下个主线任务按钮')
            game.talk_skip()