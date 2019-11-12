#!/usr/bin/env python3

""" run.py

Usage:
    run.py
    run.py public <logfile>

Options:
    --public    Server runs on a public IP (default is local only)

"""

import docopt
import logging
import logging.handlers
import os

from app import app
from app.api import setup_logging as api_setup_logging, register_bluetooth as api_register_bluetooth
from app.html_view import setup_logging as html_view_setup_logging, register_bluetooth as html_view_register_bluetooth
from app.media import setup_logging as media_setup_logging
from app.bt import BTThread, setup_logging as bt_setup_logging
from app.settings import PersistentSettings
from app.keepalive import KeepAliveThread

def get_logger():
    return logging.getLogger(__name__)


if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    settings = PersistentSettings("settings.shelve")
    
    if args['public']:
        logging_handler = logging.handlers.RotatingFileHandler(args["<logfile>"], maxBytes=1024*1024, backupCount=3)
        logging_handler.setFormatter(formatter)
        port = int(os.getenv("PROJECTOR_WEBSERVER_PORT", 8888))
        app_args = {"host": '0.0.0.0', "port": port, "debug": True}
    else:
        logging_handler = logging.StreamHandler()
        app_args = {"debug": True}

    get_logger().setLevel(logging.INFO)
    get_logger().addHandler(logging_handler)

    api_setup_logging(logging_handler)
    html_view_setup_logging(logging_handler)
    media_setup_logging(logging_handler)
    bt_setup_logging(logging_handler)
    
    bt_thread = BTThread(settings)
    bt_thread.start()

    keepalive_thread = KeepAliveThread(app.config["MEDIA_LOCATION"])
    keepalive_thread.start()

    api_register_bluetooth(bt_thread)
    html_view_register_bluetooth(bt_thread)

    app.run(**app_args, use_reloader=False)

    bt_thread.stop_thread()
    bt_thread.join()

    keepalive_thread.stop_thread()
    keepalive_thread.join()
