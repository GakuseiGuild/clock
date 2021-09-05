from PIL import Image
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
    with open(os.path.dirname(__file__) + "/../.out/name") as f:
        name = f.read()
        flag = prev_name != name and name != ""
        prev_name = name

    if flag:
        try:
            logging.info(prev_name)
            file_path = os.path.dirname(
                __file__) + "/../.out/" + str(i) + ".png"
            r, g, b = Image.open(file_path).split()
            img = Image.merge("RGB", (r, g, b)).resize((600, 448))
            epd.display(epd.getbuffer(img))

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            epd5in65f.epdconfig.module_exit()
            exit()
