""" dimmer.py

Usage:
	dimmer.py <percentage> [--dimmer=<dimmer>] [--ip=<ip>]

"""

import docopt
import requests
import time

def dimmer_get(ip, dimmer):
	resp = requests.get("http://{}/get/{}".format(ip, dimmer))
	return int(resp.text)

def dimmer_set(ip, dimmer, value):
	req = "http://{}/dimmer{}/{}".format(ip, dimmer, value)
	requests.get(req)

if __name__ == "__main__":

	args = docopt.docopt(__doc__)

	ip = args["--ip"] or "192.168.0.57"
	dimmer = args["--dimmer"] or "1"

	if int(dimmer) in [1, 2, 3, 4]:

		restore_value = dimmer_get(ip, dimmer)
		dimmer_set(ip, dimmer, args["<percentage>"])
