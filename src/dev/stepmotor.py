import math
import pigpio
import time
import threading
import warnings
from typing import NamedTuple

# ステッピングモーターのピン番号構造
class stepmotor_pin_number(NamedTuple):
    A: int
    B: int
    C: int
    D: int

# ステッピングモーターのクラス
class stepmotor():
    # 初期化
    def __init__(self,pin:stepmotor_pin_number):
        self.__pin = pin
        self.__pi1 = pigpio.pi()
        for p in pin:
            self.__pi1.set_mode(p, pigpio.OUTPUT)
        self.__number_of_per_rev = 4096
        self.__angular_velocity = 0.0
        self.__angular_velocity_max = 2*math.pi/4.0
        self.__lock = threading.RLock()
        # 各ステップでのピン出力の定義
        self.__state = [[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,1,1,0],[0,0,1,0],[0,0,1,1],[0,0,0,1],[1,0,0,1]]
        # stateのどの状態かカウントして記憶するための変数
        self.__count = 0

    def __del__(self):
        pass
    
    # 角速度取得
    @property
    def angular_velocity(self) -> float:
        with self.__lock:
            return self.__angular_velocity
    
    # 角速度設定
    @angular_velocity.setter
    def angular_velocity(self,angular_velocity:float):
        with self.__lock:
            if math.fabs(angular_velocity) > self.__angular_velocity_max:
                self.__angular_velocity = math.copysign(self.__angular_velocity_max,angular_velocity)
                warnings.warn("The specified angular velocity exceeds the upper limit.")
            else:
                self.__angular_velocity = angular_velocity
   
    # 1ステップ回転
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

    # 各ピンに出力
    def __write(self):
        for i, pin in enumerate(self.__pin):
            self.__pi1.write(pin, self.__state[self.__count][i])

    def execute(self, vel, cycle):
        dtheta = 2.0 *  math.pi / self.__number_of_per_rev
        pulse_count = int(abs(vel * cycle / dtheta))
        time.sleep(cycle / (pulse_count + 1))
        for i in range(pulse_count):
            self.__rotate_one_step(vel > 0)
            time.sleep(cycle / (pulse_count + 1))
        return pulse_count * dtheta * (1.0 if vel > 0 else -1.0)

