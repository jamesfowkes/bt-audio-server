import threading
import queue

import logging

import time
import requests

try:
    from MFRC522.MFRC522 import MFRC522
except:
    import zmq
    try:
        import rfid_faker
    except:
        import app.rfid_faker as rfid_faker 

    print("Warning: could not import MFRC522. Faking it!")

    class MFRC522Fake:

        MI_OK = 0
        PICC_REQIDL = 0

        def __init__(self, dev):
            context = zmq.Context()
            self.socket = context.socket(zmq.PAIR)
            self.socket.connect(rfid_faker.FAKE_RFID_URL)

        def MFRC522_Request(self, req):
            return (0,0)

        def MFRC522_Anticoll(self):
            try:
                uid = self.socket.recv(zmq.NOBLOCK)          
                return (self.MI_OK, uid.decode("ascii"))
            except zmq.ZMQError:
                return (None, None)

    MFRC522 = MFRC522Fake

SCAN_TIME = 0.1

def get_logger():
    return logging.getLogger(__name__)

class CardReader(threading.Thread):

    def __init__(self, device="/dev/spidev1.2", **kwargs):
        super(CardReader, self).__init__()
        self.queue = kwargs.get("queue", None)
        self.url = kwargs.get("url", None)
        self.reader = MFRC522(dev=device)
        self.runflag = True

    def run(self):

        while self.runflag:
            (_, TagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
            (status,uid) = self.reader.MFRC522_Anticoll()
            if status == self.reader.MI_OK:
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
    reader = CardReader(queue=reader_queue)
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
