import datetime
import re
from interface.repository import getConfigs, getCurrentTruth
from interface.handle_disk import loadStore
from local_types import Time, OptionalTime


time_regex = re.compile(r"(?P<minute>[0-9]*) (?P<hour>[0-9]*) (?P<day>[0-9])")


def get_alarm_time(day: datetime.date) -> OptionalTime:
    config_choice, active = getCurrentTruth(day)
    configs = getConfigs()
    if not active or config_choice == None:
        return None
    schedule_config = configs[config_choice.configId]
    return Time(schedule_config.minute, schedule_config.hour)
