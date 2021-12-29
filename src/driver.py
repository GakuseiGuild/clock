import os
import sys
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.action import demo  # nopep8
from src.dev import stepmotor


def run_action(clk, cycle):
    action = demo.Demo(clk)
    while True:
        start = time.time()
        action.execute()

        time.sleep(max(0.0, cycle - (time.time() - start)))


def run_clock(clk, cycle):
    while True:
        start = time.time()
        clk.execute()

        time.sleep(max(0.0, cycle - (time.time() - start)))

def run_long_hand(clk, cycle, pin):
    motor = stepmotor.step_motor(pin) 
    hand_dir = 0.0
    while True:
        hand_dir += motor.execute(clk.vel().long, cycle)
        clk.set_long_dir(hand_dir)

def run_short_hand(clk, cycle, pin):
    motor = stepmotor.step_motor(pin) 
    hand_dir = 0.0
    while True:
        hand_dir += motor.execute(clk.vel().short, cycle)
        clk.set_short_dir(hand_dir)

