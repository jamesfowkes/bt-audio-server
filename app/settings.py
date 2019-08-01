import shelve

import logging

def get_logger():
	return logging.getLogger(__name__)

def setup_logging(handler):
	get_logger().setLevel(logging.INFO)
	get_logger().addHandler(handler)

class PersistentSettings:

	def __init__(self, filename):
		self.__dict__["filename"] = filename
		
	def get(self, key):
		with shelve.open(self.filename) as shelf:
			try:
				v = shelf[key]
				get_logger().info("Getting {}={}".format(key, v))
				return v
			except KeyError:
				get_logger().warning("Could not get value for key {}".format(key))
				return None

	def __getitem__(self, key):
		if key == "filename":
			return self.__dict__["filename"]
		else:
			return self.get(key)
	
	def __getattr__(self, attr):
		if attr == "filename":
			return self.__dict__["filename"]

		try:
			return self.get(attr)
		except KeyError:
			raise AttributeError
	
	def __setattr__(self, name, value):
		if name == "filename":
			self.__dict__["filename"] = value
			return

		with shelve.open(self.filename) as shelf:
			get_logger().info("Setting {}={}".format(name, value))
			shelf[name] = value

	def set(self, **kwargs):
		with shelve.open(self.filename) as shelf:
			get_logger().info("Setting {} values:".format(len(kwargs)))
			for k, v in kwargs.items():
				shelf[k] = v

	def set_defaults(self, **kwargs):
		for k, v in kwargs.items():
			if self.get(k) is None:
				self.__setattr__(k, v)

