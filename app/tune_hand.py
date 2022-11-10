import keyboard
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.dev import stepmotor # nopep8

from pynput import keyboard

speed = 0.3

pin_long = stepmotor.stepmotor_pin_number(A=21,B=20,C=16,D=12)
pin_short = stepmotor.stepmotor_pin_number(A=23,B=18,C=15,D=14)

args = sys.argv
is_long = False
for arg in args:
    is_long = arg == "--long"

cycle = 1.0 / 60.0
    
motor = stepmotor.stepmotor(pin_long if is_long else pin_short) 

def on_press(key):
    try:
        print('Alphanumeric key pressed: {0} '.format(
            key.char))
        motor.execute(speed, cycle)
    except AttributeError:
        print('special key pressed: {0}'.format(
            key))

def on_release(key):
    print('Key released: {0}'.format(
        key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

while True:
    motor.execute(speed, cycle)


# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()


