import os
import sys
import threading
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src import driver  # nopep8
from src.clock import clock  # nopep8
from src.dev import stepmotor # nopep8
from src.gui import clock as gui  # nopep8
from julius import hook  # nopep8


def main():
    args = sys.argv
    # GUI を無効にするか
    is_headless = False
    for arg in args:
        is_headless = arg == "--headless"

    # 制御周期
    cycle = 1.0 / 60.0
    clk = clock.Clock(cycle)
    
    pin_long = stepmotor.stepmotor_pin_number(A=21,B=20,C=16,D=12)
    pin_short = stepmotor.stepmotor_pin_number(A=23,B=18,C=15,D=14)

    julius_output = ""
    threads = []
    if not is_headless:
        win = gui.Window(clk)
        threads.append(threading.Thread(name="gui", target=win.main))
    threads.append(threading.Thread(
        name="clock", target=driver.run_clock, args=(clk, cycle), daemon=(not is_headless)))
    #threads.append(threading.Thread(
    #    name="julius", target=hook.hook, args=(julius_output,), daemon=(not is_headless)))
    threads.append(threading.Thread(
        name="action", target=driver.run_action, args=(clk, cycle, julius_output), daemon=(not is_headless)))
    threads.append(threading.Thread(
        name="long", target=driver.run_long_hand, args=(clk, cycle, pin_long), daemon=(not is_headless)))
    threads.append(threading.Thread(
        name="short", target=driver.run_short_hand, args=(clk, cycle, pin_short), daemon=(not is_headless)))

    for th in threads:
        th.start()


if __name__ == "__main__":
    main()
