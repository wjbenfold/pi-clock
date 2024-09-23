from interface.write_store import dumpStore
from local_types import Config, Schedule, Schedules


def main():
    config_name = "weekday"
    configs = {config_name: Config(hour=7, minute=0)}
    schedules = Schedules(
        Schedule(configName=config_name),
        Schedule(configName=config_name),
        Schedule(configName=config_name),
        Schedule(configName=config_name),
        Schedule(configName=config_name),
        None,
        None,
    )
    dumpStore(configs=configs, schedules=schedules)
