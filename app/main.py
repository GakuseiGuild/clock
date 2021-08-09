import datetime
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
            now = datetime.datetime.now()
            clk.dir_long = - (now.minute / 60.0) * 2.0 * \
                math.pi + math.pi / 2.0
            clk.dir_short = -((now.hour % 12) / 12) * 2.0 * math.pi - \
                (now.minute / 60.0) * math.pi / 12.0 + math.pi / 2.0

    win = clock_gui.Window(clk)

    threads = []
    threads.append(threading.Thread(target=win.main))
    threads.append(threading.Thread(target=clk_main))
    for th in threads:
        th.start()


if __name__ == "__main__":
    main()
