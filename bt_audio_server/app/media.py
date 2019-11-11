""" media.py

Usage:
	media.py <filename>

"""

import docopt
import subprocess
import threading
import logging

audio_thread_obj = None

def get_logger():
	return logging.getLogger(__name__)

def setup_logging(handler):
	get_logger().setLevel(logging.INFO)
	get_logger().addHandler(handler)

def audio_thread(args):
	subprocess.call(args)

def play_audio(filename):

	global audio_thread_obj

	args = ["mpg123", filename]
	t = threading.Thread(target=audio_thread, args=(args, ))
	t.start()

if __name__ == "__main__":
	args = docopt.docopt(__doc__)
	play_audio(args["<filename>"])
