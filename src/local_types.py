import datetime
from typing import Dict, List, NamedTuple, TypedDict
from uuid import UUID


class Time(NamedTuple):
    minute: int
    hour: int


OptionalTime = Time | None


class Config(NamedTuple):
    name: str
    hour: int
    minute: int


Configs = Dict[UUID, Config]


class ConfigChoice(NamedTuple):
    configId: UUID


OptionalConfigChoice = ConfigChoice | None


class WeekSchedule(NamedTuple):
    mon: OptionalConfigChoice
    tues: OptionalConfigChoice
    weds: OptionalConfigChoice
    thurs: OptionalConfigChoice
    fri: OptionalConfigChoice
    sat: OptionalConfigChoice
    sun: OptionalConfigChoice


DateSchedule = Dict[datetime.date, ConfigChoice]


class FullInfo(NamedTuple):
    configs: Configs
    defaultSchedule: WeekSchedule
    overrides: DateSchedule
    active: bool


class JsonConfig(TypedDict):
    name: str
    hour: int
    minute: int


JsonDate = str  # I believe you can't use an int as the key in json

JsonSchedule = str


class JsonStore(TypedDict):
    configs: Dict[str, JsonConfig]
    defaultSchedule: List[JsonSchedule | None]
    overrides: Dict[JsonDate, JsonSchedule]
    active: bool
