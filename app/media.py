""" media.py

Usage:
	media.py <filename>

"""

import docopt
import subprocess
import threading
import logging

import app.led as led
import app.dimmer as dimmer

video_thread_obj = None
audio_thread_obj = None

stop_media_flag = False

def get_logger():
	return logging.getLogger(__name__)

def setup_logging(handler):
	get_logger().setLevel(logging.INFO)
	get_logger().addHandler(handler)

def video_thread(args):
	global stop_media_flag

	current_dimmer_value = dimmer.dimmer_get("192.168.0.57", "1")
	dimmer.dimmer_set("192.168.0.57", "1", 25)
	led.control(True)
	p = subprocess.Popen(args)

	while p.poll() is None:
		if stop_media_flag:
			get_logger().info("Terminating video")
			p.terminate()
			p.wait()

	led.control(False)
	dimmer.dimmer_set("192.168.0.57", "1", current_dimmer_value)

	stop_media_flag = False

def audio_thread(args):
	subprocess.call(args)

def stop_media():
	global stop_media_flag
	stop_media_flag = True

def play_video(filename, player):

	global video_thread_obj

	if video_thread_obj is None or not video_thread_obj.isAlive():

		get_logger().info("Firing video thread to play {}".format(filename))

		if player == "spitft":
			args = ["sudo", "SDL_VIDEODRIVER=fbcon", "SDL_FBDEV=/dev/fb1", "mplayer", "-vo", "sdl", "-framedrop", filename]
		elif player == "vlc":
			args = ["vlc", filename, "vlc://quit"]

		video_thread_obj = threading.Thread(target=video_thread, args=(args, ))
		video_thread_obj.start()
	else:
		get_logger().info("Video already playing, could not play {}".format(filename))

def play_audio(filename):
	
	global audio_thread_obj
	
	args = ["mplayer", filename]
	t = threading.Thread(target=audio_thread, args=(args, ))
	t.start()

if __name__ == "__main__":
	args = docopt.docopt(__doc__)
	play_video(args["<filename>"], "spitft")
