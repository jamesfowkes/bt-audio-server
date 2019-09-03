""" media.py

Usage:
	media.py <filename>

"""

import docopt
import subprocess
import threading

import app.led as led
import app.dimmer as dimmer

def video_thread(args):

	current_dimmer_value = dimmer.dimmer_get("192.168.0.57", "1")
	dimmer.dimmer_set("192.168.0.57", "1", 25)
	led.control(True)
	subprocess.call(args)
	led.control(False)
	dimmer.dimmer_set("192.168.0.57", "1", current_dimmer_value)

def audio_thread(args):
	subprocess.call(args)

def play_video(filename, player):

	if player == "spitft":
		args = ["sudo", "SDL_VIDEODRIVER=fbcon", "SDL_FBDEV=/dev/fb1", "mplayer", "-vo", "sdl", "-framedrop", filename]
	elif player == "vlc":
		args = ["vlc", filename, "vlc://quit"]

	t = threading.Thread(target=video_thread, args=(args, ))
	t.start()

def play_audio(filename):
	args = ["mplayer", filename]
	t = threading.Thread(target=audio_thread, args=(args, ))
	t.start()

if __name__ == "__main__":
	args = docopt.docopt(__doc__)
	play_video(args["<filename>"], "spitft")
