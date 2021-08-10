import datetime
import math
import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.action import base  # nopep8
from src.util import angle  # nopep8


class Demo(base.Base):
    def __init__(self, clk):
        super().__init__(clk)
        self.__time = time.time()
        self.__state = 0

    def execute(self):
        if self.__state == 0:
            if time.time() - self.__time > 3.0:
                self.__state = 1
                self.__time = time.time()
            self._clk.set_dial_name("")
            self._clk.set_target_dir(long=0.0, short=0.0)
        elif self.__state == 1:
            if time.time() - self.__time > 6.0:
                self.__state = 2
                self.__time = time.time()
            self._clk.set_dial_name("")
            self._clk.set_target_vel(long=-1.0, short=1.0)
        elif self.__state == 2:
            if time.time() - self.__time > 3.0:
                self.__state = 3
                self.__time = time.time()
            dir = angle.current_zodiac()
            self._clk.set_dial_name("zodiac.png")
            self._clk.set_target_dir(long=dir, short=dir)
        elif self.__state == 3:
            if time.time() - self.__time > 6.0:
                self.__state = 4
                self.__time = time.time()
            dir = angle.current_moon_age()
            self._clk.set_dial_name("moon_age.png")
            self._clk.set_target_dir(long=dir, short=dir)
        elif self.__state == 4:
            if time.time() - self.__time > 5.0:
                self.__state = 0
                self.__time = time.time()
            self._clk.set_dial_name("clock.png")
            self._clk.set_now()
        else:
            self.__state = 0
