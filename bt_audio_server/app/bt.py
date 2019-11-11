import logging
import time
import collections
import threading

from transitions import Machine

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

class BTDevice(collections.namedtuple("BTDevice", ["mac_address", "name", "paired"])):

    @classmethod
    def from_btctl_result(cls, d, paired):
        return cls(d["mac_address"], d["name"], paired)

    @classmethod
    def from_btctl_results(cls, btctl):
        
        all_devices = []

        for d in btctl.get_paired_devices():
            all_devices.append(cls.from_btctl_result(d, True))

        for d in btctl.get_discoverable_devices():
            all_devices.append(cls.from_btctl_result(d, False))

        return all_devices

    def __str__(self):
        return "{}: {} ({}paired)".format(self.name, self.mac_address, "not " if not self.paired else "")

    @property
    def select_url(self):
        return url_for("api.api_select_bt_device", mac=self.mac_address)

    @property
    def test_url(self):
        return url_for("api.api_speaker_test")


class BTThread(threading.Thread):

    states = ["idle", "scanning"]

    def __init__(self, settings):

        super(BTThread, self).__init__()
        self.btctl = Bluetoothctl()
        self.machine = Machine(model=self, states=BTThread.states, initial='waiting')
        self.machine.add_transition(trigger='start_scan', source='waiting', dest='scanning', before="start_scan_evt")
        self.machine.add_transition(trigger='start_scan', source='idle', dest='scanning', before="start_scan_evt")
        self.machine.add_transition(trigger='timeout', source='scanning', dest='idle', before="stop_scan_evt")

        self.run_flag = True

        self.paired_devices = []
        self.devices = []

        self.settings = settings

    def initial_timeout_evt(self):
        self.start_scan()

    def start_scan_evt(self):
        get_logger().info("Starting device scan")
        self.btctl.start_scan()
        self.scan_timeout = 5

    def stop_scan_evt(self):
        get_logger().info("Stopping device scan")
        self.btctl.stop_scan()
        self.update_devices()
        self.update_paired()

    def update_devices(self):
        self.devices = BTDevice.from_btctl_results(self.btctl)

    def update_paired(self):
        self.paired_devices = []
        for d in self.devices:
            if d.paired:
                self.paired_devices.append(d)

    def run(self):

        time.sleep(1)
        self.start_scan()

        while self.run_flag:
            time.sleep(1)
            if self.scan_timeout > 0:
                self.scan_timeout -= 1
                if self.scan_timeout == 0:
                    self.timeout()

    def scanning(self):
        return self.state == "scanning"

    def stop_thread(self):
        self.run_flag = False

    def last_scan_result(self):
        return self.devices

    def paired_mac_addresses(self):
        return [d.mac_address for d in self.paired_devices]

    def connect_paired(self, index):
        mac = self.paired_devices[index].mac_address
        return self.btctl.connect(mac)
    
    def has_paired_device(self):
        return len(self.paired_devices) > 0

    def busy(self):
        return self.state != "idle"

    def print_scan_results(self):
        for d in self.devices:
            print(d)

    def pair_device(self, index):
        mac = self.devices[index].mac_address
        self.btctl.pair(mac)
        self.update_devices()
        self.update_paired()

    def unpair(self, index):
        mac = self.paired_devices[index].mac_address
        self.btctl.remove(mac)
        self.update_devices()
        self.update_paired()

    def is_connected(self, index):
        mac = self.paired_devices[index].mac_address
        return self.btctl.is_connected(mac)

    def no_connection(self):
        paired_device_count = len(self.paired_devices)
        return not any([self.is_connected(i) for i in range(paired_device_count)])

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    get_logger().setLevel(logging.INFO)

    thread = BTThread()
    thread.start()

    time.sleep(0.5)
    while True:

        while thread.busy():
            pass

        if not thread.has_paired_device():
            print("No paired device. Found devices:")
            thread.print_scan_results()
            d = input("Select device to pair (1-{}) or S to rescan: ".format(len(thread.devices)))
            if d == 'S':
                thread.start_scan()
            else:
                try:
                    d = int(d)
                    if (d <= len(thread.devices)) and (d >= 1):
                        thread.pair_device(d-1)
                    else:
                        print("Invalid selection")
                except:
                    print("Invalid selection")
        elif thread.no_connection():
            print("Paired with {}".format(thread.paired_devices[0]))
            opt = input("Enter C to connect, U to unpair")
            if opt == "C":
                thread.connect_paired(0)
            elif opt == "U":
                thread.unpair(0)
        else:
            print("Connected and paired with {}".format(thread.paired_devices[0]))
            time.sleep(5.0)

    thread.stop_thread()
    thread.join()
