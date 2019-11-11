import os
import logging
import json

from flask import Blueprint, url_for, redirect

import pathlib
from collections import namedtuple

from app import app

from app.media import play_audio

AUDIO_EXTENSIONS = [".mp3", ".ogg", ".flac", ".wav"]

bt_thread = None

def get_logger():
    return logging.getLogger(__name__)

def setup_logging(handler):
    get_logger().setLevel(logging.INFO)
    get_logger().addHandler(handler)

def register_bluetooth(thread):
    global bt_thread
    bt_thread = thread

api = Blueprint('api', __name__)

class Media(namedtuple("Media", ["name", "play_url", "size_b"])):
    ''' Keeps information about a media file '''
    @classmethod
    def from_path(cls, path):
        play_url = None
        size_b = path.stat().st_size / 1024

        if path.suffix in AUDIO_EXTENSIONS:
            play_url = url_for("api.api_play_audio", filename=path.name)

        if play_url:
            return cls(path.name, play_url, size_b)

@api.route("/api/select_bt_device/<mac>")
def api_select_bt_device(mac):
    if Bluetoothctl().pair(mac):
        if Bluetoothctl().connect(mac):
            return ("Pair/connect successful", 200)
        else:
            return ("Cconnect unsuccessful", 200)
    else:
        return ("Pair unsuccessful", 500)

@api.route("/api/speaker_test")
def api_speaker_test():
    return redirect(url_for("api.api_play_audio", filename="speaker-test.wav"))

@api.route("/api/shutdown")
def api_shutdown():
    get_logger().info("Shutting down Pi")
    os.system('sudo shutdown now')
    return ("Shutting down", 200)

@api.route("/api/reboot")
def api_reboot():
    get_logger().info("Rebooting Pi")
    os.system('sudo reboot')
    return ("Rebooting", 200)

@api.route("/api/play_audio/<filename>")
def api_play_audio(filename):

    req = "/api/play_audio/{}".format(filename)
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
