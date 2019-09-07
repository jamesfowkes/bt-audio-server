import threading
import queue

import logging

import time
import requests

import serial

SCAN_TIME = 0.5

def get_logger():
    return logging.getLogger(__name__)

class RAATCardReader(threading.Thread):

    def __init__(self, device="/dev/ttyUSB0", **kwargs):
        super(RAATCardReader, self).__init__()
        self.queue = kwargs.get("queue", None)
        self.url = kwargs.get("url", None)
        self.reader = serial.Serial(device, 115200)
        time.sleep(2)
        self.runflag = True
        self.last_reply = ""

    def read_and_forget(self):
        self.reader.write("/device/01/?\r\n".encode())
        reply = self.reader.readline().decode("ascii").strip()

        if reply != "NOCARD":
            self.reader.write("/device/01/F\r\n".encode())
            self.reader.readline()

        return reply

    def run(self):

        while self.runflag:
            reply = self.read_and_forget()

            if reply != self.last_reply:
                self.last_reply = reply
                uid = reply
                get_logger().info("Reader got UID {}".format(uid))
                if self.queue:
                    get_logger().info("Putting on queue.")
                    self.queue.put(uid)
                if self.url:
                    full_url = self.url.format(uid=uid)
                    get_logger().info("Posting to URL {}".format(full_url))
                    requests.get(full_url)    
            time.sleep(SCAN_TIME)

    def stop(self):
        self.runflag = False

def setup_logging(handler):
    get_logger().setLevel(logging.INFO)
    get_logger().addHandler(handler)

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    reader_queue = queue.Queue()
    reader = RAATCardReader(queue=reader_queue)

    reader.start()

    while True:
        try:
            uid = reader_queue.get(False)
            print("New UID: {}".format(uid))
        except queue.Empty:
            pass
        except KeyboardInterrupt:
            break

    reader.stop()
    reader.join()
