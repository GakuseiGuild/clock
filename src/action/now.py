import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.action import base  # nopep8


class Now(base.Base):
    def __init__(self, clk):
        super().__init__(clk)

    def execute(self):
        self._clk.set_now()
