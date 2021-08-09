import math
import os
import sys
import time
import threading
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clock import clock  # nopep8
from src.gui import clock as gui  # nopep8


def clk_main(clk):
    cycle = 1.0 / 60.0
    while True:
        start = time.time()
        clk.set_now()

        time.sleep(max(0.0, cycle - (time.time() - start)))


def main():
    clk = clock.Clock()

    win = gui.Window(clk)

    threads = []
    threads.append(threading.Thread(name="gui", target=win.main))
    threads.append(threading.Thread(
        name="clock", target=clk_main, args=(clk,), daemon=True))
    for th in threads:
        th.start()


if __name__ == "__main__":
    main()
