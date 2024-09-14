from pathlib import Path
import re
from backend.local_types import Time


time_regex = re.compile(r"(?P<minute>[0-9]*) (?P<hour>[0-9]*) (?P<day>[0-9])")


def get_alarm_times():
    with Path("src/alarm_time.conf").open() as ff:
        rows = ff.readlines()
    for row in rows:
        match = time_regex.match(row)
        if match:
            yield Time(
                int(match["minute"]),
                int(match["hour"]),
                int(match["day"]),
            )