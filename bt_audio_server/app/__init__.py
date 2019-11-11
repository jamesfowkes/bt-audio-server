from flask import Flask

app = Flask(__name__)
app.config.from_envvar("BT_AUDIO_SERVER_CONFIG_PATH")

from app.api import api
from app.html_view import html_view

app.register_blueprint(api)
app.register_blueprint(html_view)
