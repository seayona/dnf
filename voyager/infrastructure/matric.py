import datetime
import logging
from collections import deque


# 先进先出队列
class FifoQue(object):
    def __init__(self, max=10):
        self.dq = deque()
        self.max_size = max

    def append(self, item):
        if len(self.dq) >= self.max_size:
            self.dq.popleft()
        self.dq.append(item)

    def data(self):
        return self.dq


class Matric(object):

    def __init__(self):
        self.log = logging.getLogger('Matric')
        # 创建一个日志输出器，输出到文件
        handler = logging.FileHandler('matric.log', encoding='utf-8')
        # 输入debug及以上的输出器
        handler.setLevel('INFO')
        # 格式化
        formatter = '%(asctime)s - %(levelname)s: %(message)s'
        handler.setFormatter(logging.Formatter(formatter))
        # 收集器和输出器绑定
        self.log.addHandler(handler)

        # 保存最近10条combo记录，先进先出
        self.combos = FifoQue(max=10)

    def combo(self, cls):
        message = f"【实时检测】 连击数 {(cls[1], cls[2])}"
        self.combos.append((datetime.datetime.now(), message))
        print("【Matric】",message)
