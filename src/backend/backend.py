import time

from backend.alarm_time import get_alarm_times
from backend.local_types import Time
from backend.music import shoop


def main():
    while True:
        time.sleep(5)

        now_time = time.localtime()
        now = Time(now_time.tm_min, now_time.tm_hour, now_time.tm_wday)
        print(now)

        for alarm_time in get_alarm_times():
            if now == alarm_time:
                print("Alarm fired")
                shoop()
                time.sleep(60)
