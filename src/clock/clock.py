import datetime
import math


class Clock():
    def __init__(self):
        self.__dir_long = 0.0
        self.__dir_short = 0.0

    def dir_long(self):
        return self.__dir_long

    def dir_short(self):
        return self.__dir_short

    def set_time(self, time):
        self.__dir_long = - (time.minute / 60.0) * 2.0 * \
            math.pi + math.pi / 2.0
        self.__dir_short = -((time.hour % 12) / 12) * 2.0 * math.pi - \
            (time.minute / 60.0) * math.pi / 12.0 + math.pi / 2.0

    def set_now(self):
        self.set_time(datetime.datetime.now())
