import re
from interface.write_store import loadStore
from local_types import Time, OptionalTime


time_regex = re.compile(r"(?P<minute>[0-9]*) (?P<hour>[0-9]*) (?P<day>[0-9])")


def get_alarm_time(day: int) -> OptionalTime:
    configs, schedules = loadStore()
    today_schedule = schedules[day]
    schedule_config = (
        configs[today_schedule.configName] if today_schedule != None else None
    )
    return (
        Time(schedule_config.minute, schedule_config.hour)
        if schedule_config != None
        else None
    )
