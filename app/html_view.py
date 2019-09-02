import logging
import pathlib

from flask import Blueprint, render_template

from app import app
from app.api import Video
from app.api import rfidstore

def get_logger():
    return logging.getLogger(__name__)

def setup_logging(handler):
    get_logger().setLevel(logging.INFO)
    get_logger().addHandler(handler)

html_view = Blueprint('html_view', __name__)

@html_view.route("/")
@html_view.route("/index.html")
def html_index():

    errors = []

    video_path = pathlib.Path(app.config["VIDEO_LOCATION"])
    if not video_path.exists():
        errors.append("Folder '{}' does not exist".format(video_path))

    video_files = list(video_path.glob("*"))
    video_files = [Video.from_path(v) for v in video_files]

    scan_data = {
        "lastcard": rfidstore.get_last(),
        "scantime": 0,
        "file_link" : "None",
	"files": rfidstore.file_to_card_map()
    }
    return render_template("index.html", video_path=video_path, video_files=video_files, scan_data=scan_data, errors=errors)

@html_view.route("/help.html")
def html_help():
    return render_template("help.html")


