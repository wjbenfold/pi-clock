from datetime import date
import json
from pathlib import Path
from typing import Tuple
from uuid import UUID
from local_types import (
    Config,
    Configs,
    ConfigChoice,
    FullInfo,
    WeekSchedule,
    DateSchedule,
    JsonStore,
)

filepath = Path("src/alarm_time.conf")


def makeJson(
    configs: Configs,
    defaultSchedule: WeekSchedule,
    overrides: DateSchedule,
    active: bool,
) -> JsonStore:
    jsonObject: JsonStore = {
        "configs": {
            str(key): {"name": val.name, "hour": val.hour, "minute": val.minute}
            for key, val in configs.items()
        },
        "defaultSchedule": [
            str(schedule.configId) if schedule != None else None
            for schedule in defaultSchedule
        ],
        "overrides": {
            str(date.toordinal()): str(schedule.configId)
            for date, schedule in overrides.items()
        },
        "active": active,
    }
    return jsonObject


def validateJson(jsonObject: JsonStore) -> None:
    assert (
        len(jsonObject["defaultSchedule"]) == 7
    )  # Technically rendered unnecessary by Schedules definition
    for configId in jsonObject["defaultSchedule"]:
        try:
            assert configId in jsonObject["configs"].keys() or configId is None
        except AssertionError:
            print(configId)
            raise
    for configId in jsonObject["overrides"].values():
        try:
            assert configId in jsonObject["configs"].keys() or configId is None
        except AssertionError:
            print(configId)
            raise


def readJson(jsonObject: JsonStore) -> FullInfo:
    configs = {
        UUID(key): Config(val["name"], val["hour"], val["minute"])
        for key, val in jsonObject["configs"].items()
    }
    defaultSchedule = WeekSchedule(
        *[
            ConfigChoice(UUID(configId)) if configId != None else None
            for configId in jsonObject["defaultSchedule"]
        ]
    )
    overrides = {
        date.fromordinal(int(dateOrdinal)): ConfigChoice(UUID(configId))
        for dateOrdinal, configId in jsonObject["overrides"].values()
    }

    active = jsonObject["active"]
    return FullInfo(configs, defaultSchedule, overrides, active)


def dumpStore(
    configs: Configs,
    defaultSchedule: WeekSchedule,
    overrides: DateSchedule,
    active: bool,
) -> None:
    jsonObject = makeJson(configs, defaultSchedule, overrides, active)
    validateJson(jsonObject)
    with open(filepath, "w+") as ff:
        json.dump(jsonObject, ff, indent=2)


def loadStore() -> FullInfo:
    with open(filepath, "r") as ff:
        jsonObject = json.load(ff)
    validateJson(jsonObject)
    return readJson(jsonObject)
