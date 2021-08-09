import datetime
import math
import threading
from typing import NamedTuple


class Dir(NamedTuple):
    long: float
    short: float


class Clock():
    def __init__(self):
        self.__target_dir = Dir(long=0.0, short=0.0)
        self.__lock = threading.RLock()

    def dir(self):
        with self.__lock:
            return self.__target_dir

    def set_time(self, time):
        with self.__lock:
            self.__target_dir = Dir(long=-
                                    (time.minute / 60.0) * 2.0 *
                                    math.pi + math.pi / 2.0, short=- ((time.hour % 12) / 12) * 2.0 * math.pi - (
                                        time.minute / 60.0) * math.pi / 12.0 + math.pi / 2.0)

    def set_now(self):
        self.set_time(datetime.datetime.now())
