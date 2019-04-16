import os
import datetime
import logging

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_envvar("PROJECTOR_WEBSERVER_CONFIG_PATH")

CSRFProtect(app)
Bootstrap(app)

#from app.views import standard_view
from app.api import api

#app.register_blueprint(standard_view)
app.register_blueprint(api)