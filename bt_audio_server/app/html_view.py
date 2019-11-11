import logging
import pathlib

from flask import Blueprint, render_template

from app import app
from app.api import Media

bt_thread = None

def get_logger():
    return logging.getLogger(__name__)

def setup_logging(handler):
    get_logger().setLevel(logging.INFO)
    get_logger().addHandler(handler)

def register_bluetooth(thread):
    global bt_thread
    bt_thread = thread

html_view = Blueprint('html_view', __name__)

@html_view.route("/")
@html_view.route("/index.html")
def html_index():

    errors = []

    media_path = pathlib.Path(app.config["MEDIA_LOCATION"])
    if not media_path.exists():
        errors.append("Folder '{}' does not exist".format(media_path))

    media_files = list(media_path.glob("*"))
    media_files = [Media.from_path(v) for v in media_files if v.suffix != ".json"]
    media_files = [media_file for media_file in media_files if media_file is not None]

    for file in media_files:
        get_logger().info("Found file: {}".format(str(file)))

    return render_template("index.html", media_path=media_path, media_files=media_files, errors=errors)

@html_view.route("/help.html")
def html_help():
    return render_template("help.html")

@html_view.route("/bluetooth.html")
def html_bluetooth():
    bt_thread.start_scan()
    while bt_thread.busy():
        pass

    get_logger().info("Found {} devices".format(len(bt_thread.devices)))
    return render_template("bluetooth.html", devices=bt_thread.devices)
