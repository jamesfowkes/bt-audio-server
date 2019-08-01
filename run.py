#!/usr/bin/python3

""" run.py

Usage:
    run.py <logfile> [--public]

Options:
    --public    Server runs on a public IP (default is local only)

"""

import docopt
import logging
import logging.handlers
import os

from app import app
from app.api import setup_logging as api_setup_logging
from app.html_view import setup_logging as html_view_setup_logging
#from app.settings import setup_logging as settings_setup_logging

def get_logger():
    return logging.getLogger(__name__)

if __name__ == "__main__":

    args = docopt.docopt(__doc__)

    logging_handler = logging.handlers.RotatingFileHandler(args["<logfile>"], maxBytes=1024*1024, backupCount=3)
    get_logger().setLevel(logging.INFO)
    get_logger().addHandler(logging_handler)

    api_setup_logging(logging_handler)
    html_view_setup_logging(logging_handler)
    #settings_setup_logging(logging_handler)

    if args['--public']:
        port = int(os.getenv("PROJECTOR_WEBSERVER_PORT"))
        app.run(host='0.0.0.0', port=port, debug=True)
    else:
        app.run(debug=True)

