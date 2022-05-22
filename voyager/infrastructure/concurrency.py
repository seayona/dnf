# 定义一个专门创建事件循环loop的函数，在另一个线程中启动它
import asyncio
import logging
import threading
from functools import wraps


def _start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

def asyncthrows(fn):
    @wraps(fn)
    async def asyncthrows(*args, **kwargs):
        try:
            await fn(*args, **kwargs)
        except Exception as e:
            logging.exception(e)
    return asyncthrows

def idle(fn):
    @wraps(fn)
    def _freeze(*args, **kwargs):
        self = args[0]
        if self.freezy:
            print(f'【任务调度】开始执行任务 {fn.__name__}')
            self.running = fn.__name__
            self.freezy = False
            # 在当前线程下创建时间循环，（未启用），在start_loop里面启动它
            new_loop = asyncio.new_event_loop()
            # 通过当前线程开启新的线程去启动事件循环
            t = threading.Thread(target=_start_loop, args=(new_loop,))
            t.start()
            # 运行协程
            # params = list(args)
            # del(params[0])
            asyncio.run_coroutine_threadsafe(fn(*args, **kwargs), new_loop)
            # f.result()
        else:
            print(f'【任务调度】任务{self.running}正在执行中')

    return _freeze


class Concurrency(object):
    def __init__(self):
        self.freezy = True
        self.running = None

    def _free(self):
        print('【任务调度】系统空闲')
        self.freezy = True
