import cairo
import datetime
import math
import numpy as np
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
        # 文字盤のファイル名
        self.__dial_name = "clock.png"

        self.__lock = threading.RLock()

    def dir(self):
        with self.__lock:
            return self.__dir

    def target_dir(self):
        with self.__lock:
            return self.__target_dir

    def dial_name(self):
        with self.__lock:
            return self.__dial_name

    def set_target_vel(self, target=None, long=0.0, short=0.0):
        if target == None:
            target = Dir(long=long, short=short)
        with self.__lock:
            self.__target_vel = target
            self.__target_dir = None

    def set_target_dir(self, target=None, long=0.0, short=0.0):
        if target == None:
            target = Dir(long=long, short=short)
        with self.__lock:
            self.__target_dir = target

    def set_time(self, time):
        self.set_target_dir(long=-
                            (time.minute / 60.0) * 2.0 *
                            math.pi + math.pi / 2.0, short=- ((time.hour % 12) / 12) * 2.0 * math.pi - (
                                time.minute / 60.0) * math.pi / 6.0 + math.pi / 2.0)

    def set_now(self):
        self.set_time(datetime.datetime.now())

    def set_dial_name(self, name):
        with self.__lock:
            self.__dial_name = name

    def execute_dial(self):
        AW = 600  # px 電子ペーパーの幅
        AH = 448  # px 電子ペーパーの高さ
        EW = 114.9  # mm 電子ペーパーの幅
        DIAMETER = 270.0  # 文字盤の直径

        dial_path = os.path.dirname(
            __file__) + "/../assets/" + self.__dial_name
        if os.path.isfile(dial_path):
            img = cairo.ImageSurface.create_from_png(dial_path)
            coef = (AW / img.get_width()) * (DIAMETER / EW)

            def rotation2d(dir):
                cos = np.cos(dir)
                sin = np.sin(dir)
                return np.array([[cos, -sin],
                                 [sin,  cos]])

            def make_out(theta, file_name):
                surface = cairo.ImageSurface(cairo.Format.ARGB32, AW, AH)
                ctx = cairo.Context(surface)
                ctx.scale(coef, coef)
                ctx.rotate(theta)
                ctx.translate(-img.get_width() / 2.0, -img.get_width() / 2.0)
                trans = np.dot(rotation2d(-theta),
                               np.array([17.5, 122.5]) * img.get_width() / DIAMETER)
                ctx.translate(trans[0], trans[1])
                ctx.set_source_surface(img)
                ctx.paint()
                surface.write_to_png(file_name)
            make_out(0.0, "out1.png")
            make_out(0.5 * math.pi, "out2.png")
            make_out(1.0 * math.pi, "out3.png")
            make_out(1.5 * math.pi, "out4.png")

    def execute_hands(self):
        with self.__lock:
            if self.__target_dir != None:
                # target_dir が設定されていればそれをもとに target_vel を生成
                e = angle.wrap_to_pi(
                    self.__target_dir.long - self.__dir.long)
                vel_long = math.copysign(
                    math.sqrt(2.0 * self.__acc.long * abs(e)), e)
                e = angle.wrap_to_pi(
                    self.__target_dir.short - self.__dir.short)
                vel_short = math.copysign(
                    math.sqrt(2.0 * self.__acc.short * abs(e)), e)
                self.__target_vel = Dir(long=vel_long, short=vel_short)

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

    def execute(self):
        th0 = threading.Thread(target=self.execute_dial, daemon=True)
        th1 = threading.Thread(target=self.execute_hands, daemon=True)
        th0.start()
        th1.start()
