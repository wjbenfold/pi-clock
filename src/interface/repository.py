import datetime
from typing import List, Tuple
from uuid import uuid4
from interface.handle_disk import dumpStore, loadStore
from local_types import (
    Config,
    ConfigChoice,
    Configs,
    DateSchedule,
    DateSchedule,
    OptionalConfigChoice,
    WeekSchedule,
)


def getCurrentTruths(days: List[datetime.date]) -> Tuple[DateSchedule, bool]:
    _, schedules, overrides, active = loadStore()
    currentTruth: DateSchedule = {}
    for day in days:
        if day in overrides:
            currentTruth[day] = overrides[day]
        else:
            currentTruth[day] = schedules[day.weekday()]
    return currentTruth, active


def getCurrentTruth(day: datetime.date) -> Tuple[OptionalConfigChoice, bool]:
    current_truths, active = getCurrentTruths([day])
    if day in current_truths:
        return current_truths[day], active
    else:
        return None, active


def addConfig(new_config: Config) -> None:
    current_store = loadStore()
    current_store.configs[uuid4()] = new_config
    dumpStore(
        configs=current_store.configs,
        defaultSchedule=current_store.defaultSchedule,
        overrides=current_store.overrides,
        active=current_store.active,
    )


def updateDefaultSchedule(new_schedule: WeekSchedule) -> None:
    current_store = loadStore()
    dumpStore(
        configs=current_store.configs,
        defaultSchedule=new_schedule,
        overrides=current_store.overrides,
        active=current_store.active,
    )


def setOverrides(new_truth: DateSchedule, new_active) -> None:
    configs, schedules, _, _ = loadStore()
    new_overrides = {}
    for day, config_choice in new_truth.items():
        if schedules[day.weekday()] != config_choice:
            new_overrides[day] = config_choice
    dumpStore(configs, schedules, new_overrides, new_active)


def getConfigs() -> Configs:
    return loadStore().configs
