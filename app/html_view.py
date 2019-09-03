import logging
import pathlib

from flask import Blueprint, render_template

from app import app
from app.api import Media
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

    media_path = pathlib.Path(app.config["MEDIA_LOCATION"])
    if not media_path.exists():
        errors.append("Folder '{}' does not exist".format(media_path))

    media_files = list(media_path.glob("*"))
    media_files = [Media.from_path(v) for v in media_files if v.suffix != ".json"]

    scan_data = {
        "lastcard": rfidstore.get_last(),
        "scantime": 0,
        "file_link" : "None",
	"files": rfidstore.file_to_card_map()
    }
    return render_template("index.html", media_path=media_path, media_files=media_files, scan_data=scan_data, errors=errors)

@html_view.route("/help.html")
def html_help():
    return render_template("help.html")


