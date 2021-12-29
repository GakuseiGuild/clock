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

def run_motor(clk, cycle):
    pin0 = stepmotor.step_motor_pin_number(A=26,B=19,C=13,D=6)
    pin1 = stepmotor.step_motor_pin_number(A=5,B=24,C=7,D=8)
    motor0 = stepmotor.step_motor(pin0) 
    motor1 = stepmotor.step_motor(pin1) 
    while True:
        motor0.execute(clk.vel().long, cycle)
        motor1.execute(clk.vel().short, cycle)
