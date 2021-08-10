import os
import sys
import threading
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import driver  # nopep8
from src.clock import clock  # nopep8
from src.gui import clock as gui  # nopep8


def main():
    # 制御周期
    cycle = 1.0 / 60.0
    clk = clock.Clock(cycle)

    win = gui.Window(clk)

    threads = []
    threads.append(threading.Thread(name="gui", target=win.main))
    threads.append(threading.Thread(
        name="clock", target=driver.run, args=(clk, cycle), daemon=True))
    for th in threads:
        th.start()


if __name__ == "__main__":
    main()
