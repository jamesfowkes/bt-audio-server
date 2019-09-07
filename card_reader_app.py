#!/usr/bin/env python3

import logging

from app.raat_card_reader import RAATCardReader, setup_logging as card_reader_setup_logging

def get_logger():
    return logging.getLogger(__name__)

if __name__ == "__main__":
    
    logging_handler = logging.StreamHandler()

    card_reader_url = "http://localhost:5000/api/rfid/scan/{uid}"
    
    card_reader_setup_logging(logging_handler)
    
    card_reader = RAATCardReader(url=card_reader_url)
    card_reader.run()
