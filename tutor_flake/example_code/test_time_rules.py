import time
from time import time as time_time  # noqa: TUT810

if __name__ == "__main__":
    time_time()
    time.time()  # noqa: TUT800
