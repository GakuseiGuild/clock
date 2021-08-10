import time


def run(clk, cycle):
    while True:
        start = time.time()
        clk.set_now()
        clk.execute()

        time.sleep(max(0.0, cycle - (time.time() - start)))
