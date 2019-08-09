import logging
import json

from flask import Blueprint, url_for

import pathlib
from collections import namedtuple

from app import app
#from app.settings import PersistentSettings
from app.video import play_video

from app.rfid_data import RFIDDataStore

def get_logger():
	return logging.getLogger(__name__)

def setup_logging(handler):
	get_logger().setLevel(logging.INFO)
	get_logger().addHandler(handler)
	
api = Blueprint('api', __name__)
#settings = PersistentSettings(app.config["SHELVE_FILENAME"])

rfidstore = RFIDDataStore(app.config["RFID_DATA_STORE"])

class Video(namedtuple("Video", ["name", "play_url"])):
	''' Keeps information about a video file '''
	@classmethod
	def from_path(cls, path):
		return cls(path.name, url_for("api.api_play_video", filename=path.name))

@api.route("/api/play/<filename>")
def api_play_video(filename):

	req = "/api/play/{}".format(filename)
	get_logger().info("Handling {}".format(req))

	video_path = pathlib.Path(app.config["VIDEO_LOCATION"], filename)

	response_code = 200
	if video_path.exists():
		play_video(str(video_path), app.config["VIDEO_PLAYER"])
		status = "OK"
	else:
		response_code = 404
		status = "{} not found".format(filename)

	return json.dumps(
		{
			"req": req,
			"status": status
		}
	), response_code

RFID_SCAN_URL = "/api/rfid/scan/{uid}"

@api.route("/api/rfid/scan/<uid>")
def api_scan_rfid(uid):
	req = "/api/rfid/scan/{}".format(uid)
	get_logger().info("Handling {}".format(req))

	rfidstore.log(uid)

	data = rfidstore.query(uid)
	
	if data:
		json_resp_str, response_code = api_play_video(data)
		json_resp = json.loads(json_resp_str)
		get_logger().info("Video play status: " + json_resp["status"])
		json_resp["req"] = req
		return json.dumps(json_resp), response_code

	else:
		status = "RFID {} not found".format(uid)
		get_logger().info(status)
		return json.dumps(
			{
				"req": req,
				"status": status
			}
		), 404

@api.route("/api/rfid/register/<filename>")
def api_register_rfid(filename):

	req = "/api/rfid/register/{}".format(filename)
	get_logger().info("Handling {}".format(req))

	video_path = pathlib.Path(app.config["VIDEO_LOCATION"], filename)
	response_code = 200

	if video_path.exists():
		if rfidstore.get_last() is not None:
			rfidstore.save({rfidstore.get_last() : filename})
			status = "OK"
		else:
			response_code = 404
			status = "No RFID was scanned"
			get_logger().info(status)

	else:
		response_code = 404
		status = "Video {} not found".format(filename)
		get_logger().info(status)

	return json.dumps(
		{
			"req": req,
			"status": status
		}
	), response_code