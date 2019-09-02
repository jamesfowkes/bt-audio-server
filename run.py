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
import signal

from app import app
from app.api import setup_logging as api_setup_logging
from app.api import RFID_SCAN_URL
from app.html_view import setup_logging as html_view_setup_logging
from app.card_reader import CardReader, setup_logging as card_reader_setup_logging

#from app.settings import setup_logging as settings_setup_logging

def get_logger():
    return logging.getLogger(__name__)

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    #settings_setup_logging(logging_handler)

    if args['public']:
        logging_handler = logging.handlers.RotatingFileHandler(args["<logfile>"], maxBytes=1024*1024, backupCount=3)
        port = int(os.getenv("PROJECTOR_WEBSERVER_PORT", 8888))
        app_args = {"host": '0.0.0.0', "port": port, "debug": True}
        card_reader_url = "http://0.0.0.0:{}{}".format(port,RFID_SCAN_URL)
    else:
        logging_handler = logging.StreamHandler()
        app_args = {"debug": True}
        card_reader_url = "http://localhost:5000" + RFID_SCAN_URL

    get_logger().setLevel(logging.INFO)
    get_logger().addHandler(logging_handler)

    api_setup_logging(logging_handler)
    html_view_setup_logging(logging_handler)
    card_reader_setup_logging(logging_handler)

    card_reader = CardReader(url=card_reader_url)
    card_reader.start()

    app.run(**app_args)

    get_logger().info("Application stopped, waiting for card reader...")

    card_reader.stop()
    card_reader.join()
