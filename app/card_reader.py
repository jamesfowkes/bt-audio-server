import threading
import Queue

import logging

import time

from MFRC522.MFRC522 import MFRC522

SCAN_TIME = 0.1

def get_logger():
	return logging.getLogger(__name__)

class CardReader(threading.Thread):

	def __init__(self, queue, device="/dev/spidev1.2"):
		super(CardReader, self).__init__()
		self.queue = queue
		self.reader = MFRC522(dev=device)

	def run(self):
		while True:
			(_, TagType) = self.reader.MFRC522_Request(self.reader.PICC_REQIDL)
			(status,uid) = self.reader.MFRC522_Anticoll()
			if status == self.reader.MI_OK:
				self.queue.put(uid)
			time.sleep(SCAN_TIME)

if __name__ == "__main__":

	logging.basicConfig(level=logging.INFO)

	queue = Queue.Queue()
	thread = CardReader(queue)
	thread.setDaemon(True)
	thread.start()
	while True:
		try:
			uid = queue.get(False)
			get_logger().info("New UID: %s,%s,%s,%s" % (uid[0], uid[1], uid[2], uid[3]))
		except Queue.Empty:
			pass
		except KeyboardInterrupt:
			break
