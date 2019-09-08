#!/usr/bin/env python3

""" card_reader_app.py

Usage:
    card_reader_app.py <port> <url>

"""

import logging
import docopt

from raat_card_reader import RAATCardReader, setup_logging as card_reader_setup_logging

def get_logger():
    return logging.getLogger(__name__)

if __name__ == "__main__":
    
    logging_handler = logging.StreamHandler()
    args = docopt.docopt(__doc__)

    card_reader_url = args["<url>"] + "/{uid}"

    card_reader_setup_logging(logging_handler)
    
    card_reader = RAATCardReader(device=args["<port>"], url=card_reader_url)
    card_reader.run()
