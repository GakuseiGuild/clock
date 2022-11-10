import math
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.action import base  # nopep8
from src.util import angle  # nopep8


class Fes3m33s(base.Base):
    def __init__(self, clk):
        super().__init__(clk)
        self.__changed_time = time.time()
        self.__state = 0

    def execute(self):
        # 前回の state を保存しておく
        state = self.__state

        if self.__state == 0:
            # カウント開始前の停止状態
            margin = 0.01
            start_dir_long = math.pi / 2.0
            start_dir_short = math.pi / 2.0
            if abs(self._clk.dir().long - start_dir_long) < margin and abs(self._clk.dir().short - start_dir_short) < margin:
                self.__state = 1
            self._clk.set_dial_name("20%.png")
            self._clk.set_target_dir(long=start_dir_long, short=start_dir_short)
        elif self.__state == 1:
            # カウント
            if time.time() - self.__changed_time > 10.0:
                self.__state = 0
            self._clk.set_dial_name("20%.png")
            target_dir = -(time.time() - self.__changed_time) * math.pi / 60.0 + math.pi / 2.0
            self._clk.set_target_dir(long=target_dir, short=target_dir)
        else:
            self.__state = 0

        # state が変わっていたら時刻を記録
        if self.__state != state:
            self.__changed_time = time.time()
