import datetime
import time


def sec_to_datetime(sec=None, fmt='%d/%m/%Y %H:%M:%S'):
    if sec is None:
        sec = time.time()
    return datetime.datetime.fromtimestamp(sec).strftime(fmt)


if __name__ == "__main__":
    s = 1725482668
    print(sec_to_datetime())
