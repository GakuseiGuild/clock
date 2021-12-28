import pigpio
import time
import threading
import warnings
import math
from typing import NamedTuple

class step_motor_pin_number(NamedTuple):
    A: int
    B: int
    C: int
    D: int

class step_motor():
    def __init__(self,pin:step_motor_pin_number):
        self.__pin = pin
        self.__pi1 = pigpio.pi()
        self.__pi1.set_mode(pin[0], pigpio.OUTPUT)
        self.__pi1.set_mode(pin[1], pigpio.OUTPUT)
        self.__pi1.set_mode(pin[2], pigpio.OUTPUT)
        self.__pi1.set_mode(pin[3], pigpio.OUTPUT)
        self.__number_of_per_rev = 4096
        self.__angular_velocity = 0.0
        self.__angular_velocity_max = 20*math.pi/4.0
        self.__lock = threading.RLock()
        self.__state = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
        self.__count = 0

    def __del__(self):
        pass
    
    @property
    def angular_velocity(self) -> float:
        with self.__lock:
            return self.__angular_velocity
    
    @angular_velocity.setter
    def angular_velocity(self,angular_velocity:float):
        with self.__lock:
            if math.fabs(angular_velocity) > self.__angular_velocity_max:
                self.__angular_velocity = math.copysign(self.__angular_velocity_max,angular_velocity)
                warnings.warn("The specified angular velocity exceeds the upper limit.")
            else:
                self.__angular_velocity = angular_velocity
    
    def __rotate_one_step(self,clockwise:bool):
        if clockwise:
            self.__count += 1
            if self.__count > 7:
                self.__count = 0
        else:
            self.__count -= 1
            if self.__count < 0:
                self.__count = 7
        self.__write()

    def __write(self):
        self.__pi1.write(self.__pin.A,self.__state[self.__count][0])
        self.__pi1.write(self.__pin.B,self.__state[self.__count][1])
        self.__pi1.write(self.__pin.C,self.__state[self.__count][2])
        self.__pi1.write(self.__pin.D,self.__state[self.__count][3])

    def start(self):
        while True:
            with self.__lock:
                if self.__angular_velocity > 0:
                    self.__rotate_one_step(True)
                    time.sleep(2*math.pi/self.__number_of_per_rev/math.fabs(self.__angular_velocity))
                elif self.__angular_velocity < 0:
                    self.__rotate_one_step(False)
                    time.sleep(2*math.pi/self.__number_of_per_rev/math.fabs(self.__angular_velocity))

def main():
    motor_for_long = step_motor(step_motor_pin_number(A=21,B=20,C=16,D=12))
    threads = []
    threads.append(threading.Thread(name="step_motor",target=motor_for_long.start))
    print("start")
    for th in threads:
        th.start()
    while True:
        motor_for_long.angular_velocity = 2*3.14/60
        time.sleep(1)
        motor_for_long.angular_velocity = 0
        time.sleep(1)
        motor_for_long.angular_velocity = -2*3.14/60
        time.sleep(1)
        motor_for_long.angular_velocity = 0
        time.sleep(1)
    

if __name__ == "__main__":
    main()
