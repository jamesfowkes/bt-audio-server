""" video.py

Usage:
	video.py <filename>

"""

import docopt
import subprocess

import app.led as led

def play_video(filename, player):

	if player == "spitft":
		args = ["sudo", "SDL_VIDEODRIVER=fbcon", "SDL_FBDEV=/dev/fb1", "mplayer", "-vo", "sdl", "-framedrop", filename]
	elif player == "vlc":
		args = ["vlc", filename, "vlc://quit"]

	led.control(True)
	subprocess.call(args)
	led.control(False)

if __name__ == "__main__":
	args = docopt.docopt(__doc__)
	play_video(args["<filename>"], "spitft")
