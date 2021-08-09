import math
import os
import sys
import time
import threading
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clock import clock  # nopep8
from src.gui import clock as clock_gui  # nopep8


def clk_main(clk):
    while True:
        clk.set_now()
        time.sleep(1.0 / 60.0)


def main():
    clk = clock.Clock()

    win = clock_gui.Window(clk)

    threads = []
    threads.append(threading.Thread(name="gui", target=win.main))
    threads.append(threading.Thread(
        name="clock", target=clk_main, args=(clk,), daemon=True))
    for th in threads:
        th.start()


if __name__ == "__main__":
    main()
