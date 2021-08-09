import math
import os
import sys
import threading
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.clock import clock  # nopep8
from src.gui import clock as clock_gui  # nopep8


def main():
    clk = clock.Clock()

    def clk_main():
        while True:
            clk.set_now()

    win = clock_gui.Window(clk)

    threads = []
    threads.append(threading.Thread(target=win.main))
    threads.append(threading.Thread(target=clk_main))
    for th in threads:
        th.start()


if __name__ == "__main__":
    main()
