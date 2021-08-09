import time


def run(clk):
    cycle = 1.0 / 60.0
    while True:
        start = time.time()
        clk.set_now()

        time.sleep(max(0.0, cycle - (time.time() - start)))
