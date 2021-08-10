import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.action import base  # nopep8


class Dir(base.Base):
    def __init__(self, clk):
        super().__init__(clk)
        self.__target_dir = 0.0

    def set_target_dir(self, target=None, long=0.0, short=0.0):
        if target == None:
            target = Dir(long=long, short=short)
        self.__target_dir = target

    def execute(self):
        self._clk.set_target_dir(self.__target_dir)
