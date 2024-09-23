from typing import Dict, List, NamedTuple, TypedDict


class Time(NamedTuple):
    minute: int
    hour: int


OptionalTime = Time | None


class Config(NamedTuple):
    hour: int
    minute: int


Configs = Dict[str, Config]


class Schedule(NamedTuple):
    configName: str


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
    hour: int
    minute: int


JsonSchedule = str


class JsonStore(TypedDict):
    configs: Dict[str, JsonConfig]
    schedules: List[JsonSchedule | None]
