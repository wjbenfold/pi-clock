import json
from pathlib import Path
from typing import Tuple
from uuid import UUID
from local_types import Config, Configs, Schedule, Schedules, JsonStore

filepath = Path("src/alarm_time.conf")


def makeJson(configs: Configs, schedules: Schedules) -> JsonStore:
    jsonObject: JsonStore = {
        "configs": {
            str(key): {"name": val.name, "hour": val.hour, "minute": val.minute}
            for key, val in configs.items()
        },
        "schedules": [
            str(schedule.configId) if schedule != None else None
            for schedule in schedules
        ],
    }
    return jsonObject


def validateJson(jsonObject: JsonStore) -> None:
    assert (
        len(jsonObject["schedules"]) == 7
    )  # Technically rendered unnecessary by Schedules definition
    for configId in jsonObject["schedules"]:
        try:
            assert configId in jsonObject["configs"].keys() or configId is None
        except AssertionError:
            print(configId)
            raise


def readJson(jsonObject: JsonStore) -> Tuple[Configs, Schedules]:
    configs = {
        UUID(key): Config(val["name"], val["hour"], val["minute"])
        for key, val in jsonObject["configs"].items()
    }
    schedules = Schedules(
        *[
            Schedule(UUID(configId)) if configId != None else None
            for configId in jsonObject["schedules"]
        ]
    )
    return configs, schedules


def dumpStore(configs: Configs, schedules: Schedules) -> None:
    jsonObject = makeJson(configs, schedules)
    validateJson(jsonObject)
    with open(filepath, "w+") as ff:
        json.dump(jsonObject, ff, indent=2)


def loadStore() -> Tuple[Configs, Schedules]:
    with open(filepath, "r") as ff:
        jsonObject = json.load(ff)
    validateJson(jsonObject)
    return readJson(jsonObject)


def loadJsonStore() -> JsonStore:
    return makeJson(*loadStore())
