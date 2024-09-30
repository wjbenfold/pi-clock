from uuid import uuid4
from interface.write_store import dumpStore
from local_types import Config, Schedule, Schedules


def main():
    config_name = "Weekday"
    config_id = uuid4()
    configs = {config_id: Config(name=config_name, hour=7, minute=0)}
    schedules = Schedules(
        Schedule(configId=config_id),
        Schedule(configId=config_id),
        Schedule(configId=config_id),
        Schedule(configId=config_id),
        Schedule(configId=config_id),
        None,
        None,
    )
    dumpStore(configs=configs, schedules=schedules)
