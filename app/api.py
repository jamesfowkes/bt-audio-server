import logging
import json

from flask import Blueprint, url_for

import pathlib
from collections import namedtuple

from app import app
#from app.settings import PersistentSettings
from app.media import play_video, play_audio

from app.rfid_data import RFIDDataStore

VIDEO_EXTENSIONS = [".mp4", ".m4a", ".mov"]
AUDIO_EXTENSIONS = [".mp3", ".ogg", ".flac", ".wav"]

def get_logger():
	return logging.getLogger(__name__)

def setup_logging(handler):
	get_logger().setLevel(logging.INFO)
	get_logger().addHandler(handler)

api = Blueprint('api', __name__)
#settings = PersistentSettings(app.config["SHELVE_FILENAME"])

rfidstore = RFIDDataStore(app.config["RFID_DATA_STORE"])

class Media(namedtuple("Media", ["name", "play_url", "register_url", "size_b"])):
	''' Keeps information about a media file '''
	@classmethod
	def from_path(cls, path):
		play_url = None
		register_url = url_for("api.api_register_rfid", filename=path.name)
		size_b = path.stat().st_size / 1024

		if path.suffix in VIDEO_EXTENSIONS:
			play_url = url_for("api.api_play_video", filename=path.name)
		elif path.suffix in AUDIO_EXTENSIONS:
			play_url = url_for("api.api_play_audio", filename=path.name)
		
		if play_url:
			return cls(path.name, play_url, register_url, size_b)

@api.route("/api/play_audio/<filename>")
def api_play_audio(filename):

	req = "/api/play/{}".format(filename)
	get_logger().info("Handling {}".format(req))

	audio_path = pathlib.Path(app.config["MEDIA_LOCATION"], filename)

	response_code = 200
	if audio_path.exists():
		play_audio(str(audio_path))
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

@api.route("/api/play/<filename>")
def api_play_video(filename):

	req = "/api/play/{}".format(filename)
	get_logger().info("Handling {}".format(req))

	video_path = pathlib.Path(app.config["MEDIA_LOCATION"], filename)

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

	video_path = pathlib.Path(app.config["MEDIA_LOCATION"], filename)
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
