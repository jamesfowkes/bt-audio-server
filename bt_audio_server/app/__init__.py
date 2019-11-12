from flask import Flask
import os

app = Flask(__name__)

try:
	app.config.from_envvar("BT_AUDIO_SERVER_CONFIG_PATH")
except:
	app.config.from_object("app.app_config")

from app.api import api
from app.html_view import html_view

app.register_blueprint(api)
app.register_blueprint(html_view)
