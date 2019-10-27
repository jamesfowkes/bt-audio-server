from flask import Flask

app = Flask(__name__)
app.config.from_envvar("PIGEON_WEBSERVER_CONFIG_PATH")

#from app.views import standard_view
from app.api import api
from app.html_view import html_view

#app.register_blueprint(standard_view)
app.register_blueprint(api)
app.register_blueprint(html_view)