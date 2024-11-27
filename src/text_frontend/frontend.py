import datetime
import os
from typing import Dict, List, Tuple
from uuid import UUID
from interface.handle_disk import loadStore
from interface.repository import (
    addConfig,
    getConfigs,
    getCurrentTruths,
    removeConfig,
    setOverrides,
    updateDefaultSchedule,
)

from local_types import Config, ConfigChoice, Configs, WeekSchedule

cols, lines = os.get_terminal_size()


def configsToLabels(configs: Configs) -> Dict[UUID, str]:
    uuids = [*configs.keys()]
    sorted_uuids = sorted(uuids, key=lambda x: str(x))
    return {uuid: chr(65 + ind) for ind, uuid in enumerate(sorted_uuids)}


def labelsToConfigs(configs: Configs) -> Dict[str, UUID]:
    uuids = [*configs.keys()]
    sorted_uuids = sorted(uuids, key=lambda x: str(x))
    return {chr(65 + ind): uuid for ind, uuid in enumerate(sorted_uuids)}


def parse_command(text: str):
    try:
        labToConf = labelsToConfigs(getConfigs())
        if text.startswith("nc"):
            # nc-New Config-7-30
            pieces = text.split("-")
            assert len(pieces) == 4
            name = pieces[1]
            hours = pieces[2]
            mins = pieces[3]
            addConfig(Config(name, int(hours), int(mins)))
        elif text.startswith("rm"):
            # rm-A
            pieces = text.split("-")
            assert len(pieces) == 2
            letter = pieces[1]
            removeConfig(labToConf[letter])
        elif text.startswith("sc"):
            # sc-AAAAA**
            pieces = text.split("-")
            assert len(pieces) == 2
            config = pieces[1]
            current_store = loadStore()
            config_choices = []
            for letter in config:
                if letter == "*":
                    config_choices.append(None)
                else:
                    config_choices.append(ConfigChoice(labToConf[letter]))
            new_schedule = WeekSchedule(*config_choices)
            updateDefaultSchedule(new_schedule)
        elif text.startswith("ov"):
            # ov-mon-A
            # ov-mon-*
            # ov-mon-
            # ov-off
            pieces = text.split("-")
            assert len(pieces) in [2, 3]
            current_store = loadStore()
            if len(pieces) == 2:
                if pieces[1] == "off":
                    setOverrides(current_store.overrides, False)
                else:
                    assert pieces[1] == "on"
                    setOverrides(current_store.overrides, True)
            days = get_override_dates()
            for day in days:
                if day_naming[day.weekday()].lower() == pieces[1]:
                    letter = pieces[2]
                    if letter == "":
                        new_overrides = current_store.overrides.copy()
                        new_overrides.pop(day, None)
                        setOverrides(new_overrides, current_store.active)
                    elif letter == "*":
                        new_overrides = current_store.overrides.copy()
                        new_overrides[day] = None
                        setOverrides(new_overrides, current_store.active)
                    else:
                        new_overrides = current_store.overrides.copy()
                        new_overrides[day] = ConfigChoice(labToConf[letter])
                        setOverrides(new_overrides, current_store.active)
                    break
        else:
            raise ValueError

    except (ValueError, AssertionError) as e:
        return f"Invalid input: {text}, {e}"
    return ""


def alignOnSymbol(symbol: str, strs: List[str]) -> List[str]:
    """
    Align the provided strings (strs) on the first instance of symbol in each
    """
    inds: List[Tuple[int, str]] = []
    for string in strs:
        inds.append((string.index(symbol), string))
    max_ind = max([a[0] for a in inds])
    return [" " * (max_ind - ind) + string for ind, string in inds]


def get_override_dates() -> List[datetime.date]:
    today = datetime.date.today()
    return [today + datetime.timedelta(days=ii) for ii in range(7)]


day_naming = ["Mon", "Tues", "Weds", "Thurs", "Fri", "Sat", "Sun"]


def render_config(config: Config) -> str:
    return f"{config.name} ({config.hour:02d}:{config.minute:02d})"


def render_current_state() -> List[str]:
    return_val = []
    # Configs
    return_val.append("Configs:")
    configs = getConfigs()
    confToLabel = configsToLabels(configs)
    config_lines = []
    for uuid, config in configs.items():
        config_lines.append(f"{confToLabel[uuid]}: {render_config(config)}")
    return_val += sorted(config_lines)
    return_val.append("")
    # Default schedule
    return_val.append("Default schedule:")
    defaultSchedule = loadStore().defaultSchedule
    schedule_lines = []
    schedule_lines.append(
        f"Mon: {render_config(configs[defaultSchedule.mon.configId]) if defaultSchedule.mon != None else 'None'}"
    )
    schedule_lines.append(
        f"Tues: {render_config(configs[defaultSchedule.tues.configId]) if defaultSchedule.tues != None else 'None'}"
    )
    schedule_lines.append(
        f"Weds: {render_config(configs[defaultSchedule.weds.configId]) if defaultSchedule.weds != None else 'None'}"
    )
    schedule_lines.append(
        f"Thurs: {render_config(configs[defaultSchedule.thurs.configId]) if defaultSchedule.thurs != None else 'None'}"
    )
    schedule_lines.append(
        f"Fri: {render_config(configs[defaultSchedule.fri.configId]) if defaultSchedule.fri != None else 'None'}"
    )
    schedule_lines.append(
        f"Sat: {render_config(configs[defaultSchedule.sat.configId]) if defaultSchedule.sat != None else 'None'}"
    )
    schedule_lines.append(
        f"Sun: {render_config(configs[defaultSchedule.sun.configId]) if defaultSchedule.sun != None else 'None'}"
    )
    return_val += alignOnSymbol(":", schedule_lines)
    return_val.append("")
    # Current truth
    return_val.append("Current schedule:")
    days = get_override_dates()
    schedule, active = getCurrentTruths(days)
    day_names = {day: day_naming[day.weekday()] for day in days[1:]}
    day_names[days[0]] = f"{day_naming[days[0].weekday()]} (today)"
    current_lines = []
    for day in days:
        config_choice = schedule[day]
        if config_choice == None:
            current_lines.append(f"{day_names[day]}: None")
        else:
            day_config = configs[config_choice.configId]
            current_lines.append(f"{day_names[day]}: {render_config(day_config)}")
    return_val += alignOnSymbol(":", current_lines)
    return_val.append("")
    # Active
    return_val.append(f"Alarm is currently {'ACTIVE' if active else 'INACTIVE' }")

    return return_val


def render_options() -> List[str]:
    return alignOnSymbol(
        ":",
        [
            "New config: nc-New Config-7-30",
            "Remove UNUSED config: rm-A",
            "Set week schedule: sc-AAAAA**",
            "Override day: ov-mon-A",
            "Clear override: ov-mon-",
            "Set active: ov-off",
        ],
    ) + [
        "",
        "A is the config labelled A. * is no alarm. [on,off] as active choices.",
    ]


def render_screen(err: str):
    current_state = render_current_state()
    current_state_lines = len(current_state)
    options = render_options()
    options_lines = len(options)
    if err != "":
        err_val = f"Error: {err}"
    else:
        err_val = ""
    return (
        "\n" * max(0, lines - current_state_lines - options_lines - 4)
        + "\n".join(current_state)
        + "\n\n"
        + "\n".join(options)
        + "\n"
        + "\n"
        + err_val
    )


def main():
    err = ""
    while 1:
        print(render_screen(err))
        err = parse_command(input())
