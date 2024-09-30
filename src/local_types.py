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


class Schedule(NamedTuple):
    configId: UUID


OptionalSchedule = Schedule | None


class Schedules(NamedTuple):
    mon: OptionalSchedule
    tues: OptionalSchedule
    weds: OptionalSchedule
    thurs: OptionalSchedule
    fri: OptionalSchedule
    sat: OptionalSchedule
    sun: OptionalSchedule


class JsonConfig(TypedDict):
    name: str
    hour: int
    minute: int


JsonSchedule = str


class JsonStore(TypedDict):
    configs: Dict[str, JsonConfig]
    schedules: List[JsonSchedule | None]
