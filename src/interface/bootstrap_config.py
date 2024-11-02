from uuid import uuid4
from interface.handle_disk import dumpStore
from local_types import Config, ConfigChoice, DateSchedule, WeekSchedule


def main():
    config_name = "Weekday"
    config_id = uuid4()
    configs = {config_id: Config(name=config_name, hour=7, minute=0)}
    defaultSchedule = WeekSchedule(
        ConfigChoice(configId=config_id),
        ConfigChoice(configId=config_id),
        ConfigChoice(configId=config_id),
        ConfigChoice(configId=config_id),
        ConfigChoice(configId=config_id),
        None,
        None,
    )
    overrides: DateSchedule = {}
    dumpStore(
        configs=configs,
        defaultSchedule=defaultSchedule,
        overrides=overrides,
        active=True,
    )
