from datetime import date
import subprocess
import time

from backend.alarm_time import get_alarm_time
from local_types import Time
from backend.music import shoop


def main():
    while True:
        time.sleep(5)

        now_time = time.localtime()
        now = Time(now_time.tm_min, now_time.tm_hour)
        today = date.today()

        if now == get_alarm_time(today):
            print("Alarm fired")
            shoop()
            time.sleep(300)
