import math


def wrap_to_2pi(r):
    return math.fmod(r, 2.0 * math.pi)


def wrap_to_pi(r):
    wrapped = math.fmod(r, 2.0 * math.pi)
    if wrapped > math.pi:
        wrapped -= 2.0 * math.pi
    elif wrapped <= -math.pi:
        wrapped += 2.0 * math.pi
    return wrapped
