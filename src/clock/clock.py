import cairo
import datetime
import fcntl
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
        # 制御を進行するか
        self.run_flag = False
        self.button_1_clicked = False
        self.button_2_clicked = False
        # 制御周期
        self.__cycle = cycle
        # 加速度制限 [rad/s^2]
        self.__acc = Dir(long=1.0, short=1.0)
        # 速度制限 [rad/s]
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
        self.__dial_name = "none.png"
        # 文字盤を出力したか
        self.__dial_output = True

        self.__lock = threading.RLock()

    def target_vel(self):
        with self.__lock:
            return self.__target_vel

    def vel(self):
        with self.__lock:
            return self.__vel

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

    def set_dir(self, dir=None, long=0.0, short=0.0):
        if dir == None:
            dir = Dir(long=long, short=short)
        with self.__lock:
            self.__dir = dir
    
    def set_long_dir(self, long_dir):
        with self.__lock:
            self.__dir = Dir(long=long_dir, short=self.__dir.short)

    def set_short_dir(self, short_dir):
        with self.__lock:
            self.__dir = Dir(long=self.__dir.long, short=short_dir)

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
        if name == "":
            name = "none.png"
        if name != self.__dial_name:
            with self.__lock:
                self.__dial_name = name
                self.__dial_output = False

    def tune_long_left(self):
        self.set_long_dir(angle.wrap_to_2pi(self.__dir.long + 0.05))

    def tune_long_right(self):
        self.set_long_dir(angle.wrap_to_2pi(self.__dir.long - 0.05))

    def tune_short_left(self):
        self.set_short_dir(angle.wrap_to_2pi(self.__dir.short + 0.05))

    def tune_short_right(self):
        self.set_short_dir(angle.wrap_to_2pi(self.__dir.short - 0.05))

    def execute_dial(self):
        AW = 600  # px 電子ペーパーの幅
        AH = 448  # px 電子ペーパーの高さ
        EW = 114.9  # mm 電子ペーパーの幅
        DIAMETER = 270.0  # 文字盤の直径

        if self.__dial_output == True:
            return
        dial_path = os.path.dirname(
            __file__) + "/../assets/pic/" + self.__dial_name
        if os.path.isfile(dial_path):
            try:
                img = cairo.ImageSurface.create_from_png(dial_path)
                coef = (AW / img.get_width()) * (DIAMETER / EW)

                def rotation2d(dir):
                    cos = np.cos(dir)
                    sin = np.sin(dir)
                    return np.array([[cos, -sin],
                                    [sin,  cos]])

                os.makedirs(os.path.dirname(__file__) +
                            "/../../.out/", exist_ok=True)

                def make_out(theta, file_name):
                    surface = cairo.ImageSurface(cairo.Format.ARGB32, AW, AH)
                    ctx = cairo.Context(surface)
                    ctx.scale(coef, coef)
                    ctx.rotate(theta)
                    ctx.translate(-img.get_width() / 2.0, -
                                  img.get_width() / 2.0)
                    trans = np.dot(rotation2d(-theta),
                                   np.array([17.5, 122.5]) * img.get_width() / DIAMETER)
                    ctx.translate(trans[0], trans[1])
                    ctx.set_source_surface(img)
                    ctx.paint()
                    file_path = os.path.dirname(
                        __file__) + "/../../.out/" + file_name
                    with open(file_path, "wb") as f:
                        fcntl.flock(f, fcntl.LOCK_EX)
                        surface.write_to_png(file_path)
                        fcntl.flock(f, fcntl.LOCK_UN)
                make_out(0.0, "1.png")
                make_out(0.5 * math.pi, "2.png")
                make_out(1.0 * math.pi, "3.png")
                make_out(1.5 * math.pi, "4.png")
                self.__dial_output = True
                for i in range(1, 5):
                    with open(os.path.dirname(__file__) + "/../../.out/name" + str(i), "w") as f:
                        f.write(self.__dial_name)
            except:
                pass

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
            # self.__dir = Dir(long=long, short=short)

    def execute(self):
        th0 = threading.Thread(target=self.execute_dial, daemon=True)
        th1 = threading.Thread(target=self.execute_hands, daemon=True)
        th0.start()
        th1.start()
        th0.join()
        th1.join()
