import math
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.action import base  # nopep8
from src.util import angle  # nopep8


class Voice(base.Base):
    def __init__(self, clk, julius_output):
        super().__init__(clk)
        self.__changed_time = time.time()
        self.__state = 0
        self.__julius_output = julius_output

    def execute(self):
        # 前回の state を保存しておく
        state = self.__state

        if self.__julius_output != "":
            print(self.__julius_output)

        if self.__julius_output == "show_zodiac":
            self.__state = 2
        elif self.__julius_output == "show_ moonage":
            self.__state = 3
        elif self.__julius_output == "show_time":
            self.__state = 4

        if self.__state == 0:
            self._clk.set_dial_name("")
            self._clk.set_target_dir(long=math.pi, short=math.pi)
        elif self.__state == 1:
            self._clk.set_dial_name("")
            self._clk.set_target_dir(long=0.0, short=0.0)
        elif self.__state == 2:
            dir = angle.current_zodiac()
            self._clk.set_dial_name("zodiac.png")
            self._clk.set_target_dir(long=dir, short=dir)
        elif self.__state == 3:
            dir = angle.current_moon_age()
            self._clk.set_dial_name("moon_age.png")
            self._clk.set_target_dir(long=dir, short=dir)
        elif self.__state == 4:
            self._clk.set_dial_name("clock.png")
            self._clk.set_now()
        else:
            self.__state = 0

        # state が変わっていたら時刻を記録
        if self.__state != state:
            self.__changed_time = time.time()
