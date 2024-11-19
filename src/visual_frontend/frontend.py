import datetime
from typing import Dict, List
from uuid import UUID
from flask import abort, Flask, render_template, redirect, request

from interface.handle_disk import loadStore
from interface.repository import (
    addConfig,
    getConfigs,
    getCurrentTruths,
    setOverrides,
    updateDefaultSchedule,
)
from local_types import (
    Config,
    Configs,
    ConfigChoice,
    DateSchedule,
    DateSchedule,
    WeekSchedule,
)

NONE_ID = UUID("937defb6-837e-4cf0-a250-08ec57e682ee")

app = Flask(__name__)


@app.route("/", methods=["GET"])
def root():
    return handle_root_get()


@app.route("/overrides", methods=["POST"])
def overrides():
    handle_overrides_post()
    return redirect("/")


@app.route("/configs", methods=["GET", "POST"])
def post_configs():
    match request.method:
        case "GET":
            return handle_configs_get()
        case "POST":
            return handle_configs_post()
    return redirect("/")


def handle_configs_get():
    configs = getConfigs()
    return render_template("configs.html", configs=configs)


def handle_configs_post():
    name = request.form.get("name")
    hours = request.form.get("hours")
    minutes = request.form.get("minutes")
    if name == None or hours == None or minutes == None:
        abort(400)
    try:
        num_hours = int(hours)
        num_minutes = int(minutes)
    except ValueError:
        abort(400)
    addConfig(Config(name, num_hours, num_minutes))
    return redirect("/configs")


@app.route("/schedules", methods=["GET", "POST"])
def post_schedules():
    match request.method:
        case "GET":
            return handle_schedules_get()
        case "POST":
            return handle_schedules_post()
    return redirect("/")


def handle_schedules_get():
    current_store = loadStore()
    return render_template(
        "schedules.html",
        configs=get_jinja_configs(current_store.configs),
        schedules=get_jinja_schedules(current_store.defaultSchedule),
    )


def get_jinja_configs(configs: Configs) -> Dict[UUID, str]:
    return {key: conf.name for key, conf in configs.items()} | {NONE_ID: "None"}


def get_jinja_schedules(schedules: WeekSchedule) -> WeekSchedule:
    return WeekSchedule(
        *[
            ConfigChoice(x.configId) if x is not None else ConfigChoice(NONE_ID)
            for x in schedules
        ]
    )


def handle_schedules_post():
    results = [
        request.form.get("mon"),
        request.form.get("tues"),
        request.form.get("weds"),
        request.form.get("thurs"),
        request.form.get("fri"),
        request.form.get("sat"),
        request.form.get("sun"),
    ]
    if None in results:
        abort(400)
    else:
        updateDefaultSchedule(
            WeekSchedule(
                *[
                    ConfigChoice(UUID(result))
                    if result != str(NONE_ID) and result is not None
                    else None
                    for result in results
                ]
            )
        )
    return redirect("/schedules")


def get_override_dates() -> List[datetime.date]:
    today = datetime.date.today()
    return [today + datetime.timedelta(days=ii) for ii in range(7)]


day_naming = ["Mon", "Tues", "Weds", "Thurs", "Fri", "Sat", "Sun"]


def handle_root_get():
    days = get_override_dates()
    schedule, active = getCurrentTruths(days)
    day_names = {day: day_naming[day.weekday()] for day in days[1:]}
    day_names[days[0]] = f"{day_naming[days[0].weekday()]} (today)"
    return render_template(
        "index.html",
        configs=get_jinja_configs(getConfigs()),
        current_truths=get_jinja_current_truths(schedule),
        active=active,
        days=days,
        day_names=day_names,
    )


def get_jinja_current_truths(schedule: DateSchedule) -> DateSchedule:
    jinja_schedule = {}
    for day in schedule.keys():
        config_choice = schedule[day]
        if config_choice is not None:
            jinja_schedule[day] = config_choice
        else:
            jinja_schedule[day] = ConfigChoice(NONE_ID)
    return jinja_schedule


def handle_overrides_post():
    days = get_override_dates()
    overrides: DateSchedule = {}
    for day in days:
        result = request.form.get(str(day))
        overrides[day] = (
            ConfigChoice(UUID(result))
            if result != str(NONE_ID) and result is not None
            else None
        )
    is_active = "active" in request.form
    setOverrides(overrides, is_active)


def main():
    app.run(host="0.0.0.0", port=8080)
