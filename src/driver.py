import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.action import fes3m33s  # nopep8
from src.action import demo  # nopep8
from src.action import voice  # nopep8
from src.dev import stepmotor
from src.util import angle


def run_action(clk, cycle, julius_output):
    action = fes3m33s.Fes3m33s(clk)
    #action = demo.Demo(clk)
    #action = voice.Voice(clk, julius_output)
    while True:
        if clk.run_flag:
            start = time.time()
            action.execute()

            time.sleep(max(0.0, cycle - (time.time() - start)))


def run_clock(clk, cycle):
    while True:
        if clk.run_flag:
            start = time.time()
            clk.execute()

            time.sleep(max(0.0, cycle - (time.time() - start)))


def run_long_hand(clk, cycle, pin):
    motor = stepmotor.stepmotor(pin) 
    while True:
        if clk.run_flag:
            hand_dir = angle.wrap_to_2pi(clk.dir().long + motor.execute(clk.vel().long, cycle))
            clk.set_long_dir(hand_dir)


def run_short_hand(clk, cycle, pin):
    motor = stepmotor.stepmotor(pin) 
    while True:
        if clk.run_flag:
            hand_dir = angle.wrap_to_2pi(clk.dir().short + motor.execute(clk.vel().short, cycle))
            clk.set_short_dir(hand_dir)

