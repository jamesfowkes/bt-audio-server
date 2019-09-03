class GPIOFake:
	OUT = 0
	BCM = 0
	HIGH = 0
	LOW = 0
	BOARD = 0
	
	def setmode(self, mode):
		pass
	def setup(self, pin, mode):
		pass
	def output(self, pin, level):
		pass
	def cleanup(self):
		pass
		