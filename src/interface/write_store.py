import json
from pathlib import Path
from typing import Dict, Tuple
from local_types import Config, Configs, Schedule, Schedules, JsonStore

filepath = Path("src/alarm_time.conf")


def makeJson(configs: Dict[str, Config], schedules: Schedules) -> JsonStore:
    jsonObject: JsonStore = {
        "configs": {
            key: {"hour": val.hour, "minute": val.minute}
            for key, val in configs.items()
        },
        "schedules": [
            schedule.configName if schedule != None else None for schedule in schedules
        ],
    }
    return jsonObject


def validateJson(jsonObject: JsonStore) -> None:
    assert (
        len(jsonObject["schedules"]) == 7
    )  # Technically rendered unnecessary by Schedules definition
    for configName in jsonObject["schedules"]:
        try:
            assert configName in jsonObject["configs"].keys() or configName is None
        except AssertionError:
            print(configName)
            raise


def readJson(jsonObject: JsonStore) -> Tuple[Configs, Schedules]:
    configs = {
        key: Config(val["hour"], val["minute"])
        for key, val in jsonObject["configs"].items()
    }
    schedules = Schedules(
        *[
            Schedule(configName) if configName != None else None
            for configName in jsonObject["schedules"]
        ]
    )
    return configs, schedules


def dumpStore(configs: Configs, schedules: Schedules) -> None:
    jsonObject = makeJson(configs, schedules)
    validateJson(jsonObject)
    with open(filepath) as ff:
        json.dump(jsonObject, ff)


def loadStore() -> Tuple[Configs, Schedules]:
    with open(filepath) as ff:
        jsonObject = json.load(ff)
    validateJson(jsonObject)
    return readJson(jsonObject)


def loadJsonStore() -> JsonStore:
    return makeJson(*loadStore())
