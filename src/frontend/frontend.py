import json
from typing import Dict, List
from flask import abort, Flask, render_template, redirect, url_for, request

from interface.write_store import dumpStore, loadStore
from local_types import Config, Configs, Schedule, Schedules

app = Flask(__name__)


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/configs", methods=["GET", "POST"])
def post_configs():
    match request.method:
        case "GET":
            return handle_configs_get()
        case "POST":
            return handle_configs_post()
    return redirect("/")


def handle_configs_get():
    configs, _ = loadStore()
    return render_template("configs.html", configs=configs)


def handle_configs_post():
    configs, schedules = loadStore()
    name = request.form.get("name")
    hours = request.form.get("hours")
    minutes = request.form.get("minutes")
    if name == None or hours == None or minutes == None:
        abort(400)
    new_config = Config(int(hours), int(minutes))
    configs[name] = new_config
    dumpStore(configs=configs, schedules=schedules)
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
    configs, schedules = loadStore()
    return render_template(
        "schedules.html",
        config_list=get_jinja_config_list(configs),
        schedules=get_jinja_schedule_list(schedules),
    )


def get_jinja_config_list(configs: Configs) -> List[str]:
    return ["None"] + list(configs.keys())


def get_jinja_schedule_list(schedules: Schedules) -> Schedules:
    return Schedules(
        *[
            Schedule(x.configName) if x is not None else Schedule("None")
            for x in schedules
        ]
    )


def handle_schedules_post():
    configs, _ = loadStore()
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
        new_schedules = Schedules(
            *[
                Schedule(result) if result != "None" and result is not None else None
                for result in results
            ]
        )
        dumpStore(configs=configs, schedules=new_schedules)
    return redirect("/schedules")


def main():
    app.run(port=8080)
