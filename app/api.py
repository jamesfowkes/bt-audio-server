import logging
import json

from flask import Blueprint, url_for

import pathlib
from collections import namedtuple

from app import app
#from app.settings import PersistentSettings
from app.video import play_video

def get_logger():
	return logging.getLogger(__name__)

def setup_logging(handler):
	get_logger().setLevel(logging.INFO)
	get_logger().addHandler(handler)
	
api = Blueprint('api', __name__)
#settings = PersistentSettings(app.config["SHELVE_FILENAME"])

class Video(namedtuple("Video", ["name", "play_url"])):
	''' Keeps information about a video file '''
	@classmethod
	def from_path(cls, path):
		return cls(path.name, url_for("api.api_play_video", filename=path.name))


@api.route("/api/rfid/read")
def api_read_rfid():
	get_logger().info("Handling /api/rfid/read/")

	return json.dumps(
		{
			"req":"/api/rfid/read/",
			"rfid": ""
		}
	)

@api.route("/api/play/<filename>")
def api_play_video(filename):

	req = "/api/play/{}".format(filename)
	get_logger().info("Handling {}".format(req))

	video_path = pathlib.Path(app.config["VIDEO_LOCATION"], filename)

	response_code = 200
	if video_path.exists():
		play_video(str(video_path), app.config["VIDEO_PLAYER"])
		status = ""
	else:
		response_code = 404
		status = "{} not found".format(filename)

	return json.dumps(
		{
			"req": req,
			"status": status
		}
	), response_code
