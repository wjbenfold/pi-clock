import json
from flask import Flask, render_template, redirect, url_for, request

from interface.write_store import loadJsonStore, loadStore

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
            handle_configs_post()
    return redirect(url_for("/"))


def handle_configs_get():
    configs, _ = loadStore()
    return render_template("configs.html", configs=configs)


def handle_configs_post():
    configs = loadJsonStore()["configs"]
    configs[request.form["name"]] = json.loads(request.form["config"])


@app.route("/schedules", methods=["GET", "POST"])
def post_schedules():
    match request.method:
        case "GET":
            return handle_schedules_get()
        case "POST":
            handle_schedules_post()
    return redirect(url_for("/"))


def handle_schedules_get():
    configs, schedules = loadStore()
    return render_template("schedules.html", configs=configs, schedules=schedules)


def handle_schedules_post():
    pass


def main():
    app.run(port=8080)
