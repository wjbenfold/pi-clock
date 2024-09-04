from pathlib import Path
import time

from alarm_time import get_alarm_times
from local_types import Time
from music import shoop


def main():
    while not Path("exit.flg").is_file():
        time.sleep(5)

        now_time = time.localtime()
        now = Time(now_time.tm_min, now_time.tm_hour, now_time.tm_wday)
        print(now)

        for alarm_time in get_alarm_times():
            if now == alarm_time:
                print("Alarm fired")
                shoop()
                time.sleep(60)


main()
