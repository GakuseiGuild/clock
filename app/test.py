from PIL import Image
import logging
import os
import sys
import threading
import wiringpi
import RPi.GPIO
libdir = os.path.join(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))), "e-Paper/RaspberryPi_JetsonNano/python/lib")
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd5in65f  # nopep8

logging.basicConfig(level=logging.DEBUG)

# 電子ペーパーの [位置，CS ピン]
positions = [[1, 7], [2, 8], [3, 9], [4, 10]]

lock = threading.RLock()

def display_epaper(pos):
    prev_name = ""
    flag = False
    epd = epd5in65f.EPD()
    epd.init()

    # CS
    cs_pin = pos[1]
    epd.cs_pin(cs_pin)
    GPIO = RPi.GPIO
    GPIO.setup(cs_pin, GPIO.OUT)
    wiringpi.digitalWrite(cs_pin, 1)

    while True:
        with open(os.path.dirname(__file__) + "/../.out/name") as f:
            name = f.read()
            flag = prev_name != name and name != ""
            prev_name = name

        if flag:
            try:
                logging.info(prev_name)
                file_path = os.path.dirname(
                    __file__) + "/../.out/" + str(pos[0]) + ".png"
                r, g, b = Image.open(file_path).split()
                img = Image.merge("RGB", (r, g, b)).resize((600, 448))
                with lock:
                    wiringpi.digitalWrite(cs_pin, 0)
                    epd.display(epd.getbuffer(img))
                    wiringpi.digitalWrite(cs_pin, 1)

            except IOError as e:
                logging.info(e)

            except KeyboardInterrupt:
                logging.info("ctrl + c:")
                epd5in65f.epdconfig.module_exit()
                exit()

threads = []
for pos in positions:
    threads.append(threading.Thread(target=display_epaper, args=(pos)))
for thread in threads:
    thread.start()
