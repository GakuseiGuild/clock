from PIL import Image
import time
import logging
import sys
import os
libdir = os.path.join(os.path.dirname(os.path.dirname(
    os.path.realpath(__file__))), "../e-Paper/RaspberryPi_JetsonNano/python/lib")
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd5in65f  # nopep8

logging.basicConfig(level=logging.DEBUG)

# 電子ペーパーの位置
i = 2

prev_name = ""
flag = False
epd = epd5in65f.EPD()
epd.init()

while True:
    file_path = os.path.dirname(__file__) + "/../.out/name"
    with open(file_path) as f:
        name = f.read()
        flag = prev_name != name and name != ""
        prev_name = name

    if flag:
        try:
            logging.info(prev_name)
            file_path = os.path.dirname(__file__) + "/../.out/" + str(i)
            img = Image.open(file_path + ".png")
            r, g, b = img.split()
            img = Image.merge("RGB", (r, g, b))
            img = img.resize((600, 448))
            img.save(file_path + ".bmp")

            Himage = Image.open(file_path + ".bmp")
            epd.display(epd.getbuffer(Himage))

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd5in65f.epdconfig.module_exit()
            exit()
