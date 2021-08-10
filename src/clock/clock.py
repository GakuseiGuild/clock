import datetime
import math
import os
import sys
import threading
from typing import NamedTuple
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.util import angle  # nopep8


class Dir(NamedTuple):
    long: float
    short: float


class Clock():
    def __init__(self, cycle):
        # 制御周期
        self.__cycle = cycle
        # 加速度制限 [rad/s^2]
        self.__acc = Dir(long=1.0, short=1.0)
        # 速度制限 [rad/s^2]
        self.__vel_max = Dir(long=1.0, short=1.0)
        # 目標速度 [rad/s]
        self.__target_vel = Dir(long=0.0, short=0.0)
        # 速度 [rad/s]
        self.__vel = Dir(long=0.0, short=0.0)
        # 角度 [rad]
        self.__dir = Dir(long=0.0, short=0.0)
        # 目標角度 [rad]
        self.__target_dir = self.__dir

        self.__lock = threading.RLock()

    def dir(self):
        with self.__lock:
            return self.__dir

    def target_dir(self):
        with self.__lock:
            return self.__target_dir

    def set_target_vel(self, target):
        with self.__lock:
            self.__target_vel = target
            self.__target_dir = None

    def set_target_dir(self, target):
        with self.__lock:
            self.__target_dir = target
            e = angle.wrap_to_pi(
                self.__target_dir.long - self.__dir.long)
            vel_long = math.copysign(
                math.sqrt(2.0 * self.__acc.long * abs(e)), e)
            e = angle.wrap_to_pi(
                self.__target_dir.short - self.__dir.short)
            vel_short = math.copysign(
                math.sqrt(2.0 * self.__acc.short * abs(e)), e)
            self.__target_vel = Dir(long=vel_long, short=vel_short)

    def set_time(self, time):
        self.set_target_dir(Dir(long=-
                                (time.minute / 60.0) * 2.0 *
                                math.pi + math.pi / 2.0, short=- ((time.hour % 12) / 12) * 2.0 * math.pi - (
                                    time.minute / 60.0) * math.pi / 6.0 + math.pi / 2.0))

    def set_now(self):
        self.set_time(datetime.datetime.now())

    def execute(self):
        with self.__lock:
            e = angle.wrap_to_pi(self.__target_vel.long - self.__vel.long)
            acc = 0.0 if e == 0.0 else math.copysign(self.__acc.long, e)
            vel_long = self.__vel.long + self.__cycle * acc
            e = angle.wrap_to_pi(self.__target_vel.short - self.__vel.short)
            acc = 0.0 if e == 0.0 else math.copysign(self.__acc.short, e)
            vel_short = self.__vel.short + self.__cycle * acc
            vel_long = math.copysign(
                min(abs(vel_long), self.__vel_max.long), vel_long)
            vel_short = math.copysign(
                min(abs(vel_short), self.__vel_max.short), vel_short)
            self.__vel = Dir(vel_long, vel_short)
            long = angle.wrap_to_2pi(
                self.__dir.long + self.__cycle * self.__vel.long)
            short = angle.wrap_to_2pi(
                self.__dir.short + self.__cycle * self.__vel.short)
            self.__dir = Dir(long=long, short=short)
