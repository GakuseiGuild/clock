import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clock import clock  # nopep8


def run(clk, cycle):
    while True:
        start = time.time()
        clk.set_target_vel(clock.Dir(long=1.0, short=-1.0))
        clk.execute()

        time.sleep(max(0.0, cycle - (time.time() - start)))
