import logging
import time
import collections

from flask import url_for

try:
	from app.bluetoothctl import Bluetoothctl
except:
	from bluetoothctl import Bluetoothctl

def get_logger():
	return logging.getLogger(__name__)

def setup_logging(handler):
	get_logger().setLevel(logging.INFO)
	get_logger().addHandler(handler)

class BTDevice(collections.namedtuple("BTDevice", ["MAC", "name", "select_url", "paired"])):

	@classmethod
	def from_btctl_result(cls, d, paired):
		return cls(d["mac_address"], d["name"], url_for("api.api_select_bt_device", mac=d["mac_address"]), paired)

	@classmethod
	def scan_now(cls):
		btctl = Bluetoothctl()
		btctl.start_scan()
		time.sleep(5)
		btctl.stop_scan()
		paired_devices = [cls.from_btctl_result(d, True) for d in btctl.get_paired_devices()]
		discoverable_devices = [cls.from_btctl_result(d, False) for d in btctl.get_discoverable_devices()]

		return paired_devices + discoverable_devices
	
if __name__ == "__main__":

	devices = BTDevice.scan_now()

	if len(devices):
		for d in devices:
			print("{} {}{}".format(d["name"], d["mac_address"], " (paired)" if d.paired else ""))
	else:
		print("No devices found")
