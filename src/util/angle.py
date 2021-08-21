import datetime
import ephem
import math
import requests
from pytz import timezone


def wrap_to_2pi(r):
    return math.fmod(r, 2.0 * math.pi)


def wrap_to_pi(r):
    wrapped = math.fmod(r, 2.0 * math.pi)
    if wrapped > math.pi:
        wrapped -= 2.0 * math.pi
    elif wrapped <= -math.pi:
        wrapped += 2.0 * math.pi
    return wrapped


def zodiac(datetime=None, year=2021):
    if datetime != None:
        year = datetime.year
    return -(year % 12 - 4) * math.pi / 6.0 + math.pi / 2.0


def current_zodiac():
    return zodiac(year=datetime.datetime.now().year)


def moon_age(datetime):
    utc = timezone("Asia/Tokyo").localize(datetime).astimezone(timezone("UTC"))

    previous_new_moon_time_jst = timezone("UTC").localize(ephem.previous_new_moon(utc).datetime()).astimezone(
        timezone("Asia/Tokyo"))

    moon_age = timezone("Asia/Tokyo").localize(datetime) - \
        previous_new_moon_time_jst
    moon_age = round(moon_age.days + moon_age.seconds / (60 * 60 * 24.0), 1)
    return (moon_age / 31.0) * 2.0 * math.pi + math.pi / 2.0


def current_moon_age():
    return moon_age(datetime.datetime.now())


def weather(area_name):
    url = 'https://www.jma.go.jp/bosai/forecast/data/forecast/010000.json'
    data = requests.get(url).json()
    for area in data:
        name = area['name']
        if name == area_name:
            for ts in area['srf']['timeSeries']:
                if 'weathers' in ts['areas']:
                    for i, v in enumerate(ts['areas']['weathers']):
                        return v
    return
