""" rfid_faker.py

Usage:
	rfid_faker.py <uid>

"""

import docopt
import zmq

FAKE_RFID_URL = "ipc:///tmp/rfidfake"

if __name__ == "__main__":

	args = docopt.docopt(__doc__)

	context = zmq.Context()
	socket = context.socket(zmq.PAIR)
	socket.bind(FAKE_RFID_URL)
	socket.send(args["<uid>"].encode("ascii"))
