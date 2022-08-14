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

logging.basicConfig(level=logging.INFO)

# 電子ペーパーの [位置，CS ピン, BUSY ピン]
positions = [[1, 2, 6], [2, 3, 13], [3, 4, 19], [4, 17, 26]]

lock = threading.RLock()

# Other
reset_pin = 27
dc_pin = 25

def display_epaper(pos, cs_pin, busy_pin):
    prev_name = ""
    flag = False
    epd = epd5in65f.EPD()

    GPIO = RPi.GPIO
    GPIO.setmode(GPIO.BCM)
    # CS
    epd.cs_pin = cs_pin
    GPIO.setup(cs_pin, GPIO.OUT)
    wiringpi.digitalWrite(cs_pin, 1)
    # BUSY
    epd.busy_pin = busy_pin
    GPIO.setup(busy_pin, GPIO.IN)
    # Other
    epd.reset_pin = 27
    epd.dc_pin = 25
    GPIO.setup(epd.reset_pin, GPIO.OUT)
    GPIO.setup(epd.dc_pin, GPIO.OUT)

    epd.init()

    file_path = os.path.dirname(
        os.path.abspath("__file__")) + "/.out/" + str(pos) + ".png"
    while True:
        with open(os.path.dirname(os.path.abspath("__file__")) + "/.out/name" + str(pos)) as f:
            name = f.read()
            flag = prev_name != name and name != ""
            prev_name = name

        if flag:
            try:
                logging.info(str(pos) + ": " + prev_name)
                r, g, b = Image.open(file_path).split()
                img = Image.merge("RGB", (r, g, b)).resize((600, 448))
                epd.display(epd.getbuffer(img), lock)

            except IOError as e:
                logging.info(e)

            except KeyboardInterrupt:
                logging.info("ctrl + c:")
                epd5in65f.epdconfig.module_exit()
                exit()
            except:
                pass

threads = []
for pos in positions:
    threads.append(threading.Thread(target=display_epaper, args=(pos[0], pos[1], pos[2])))
for thread in threads:
    thread.start()
