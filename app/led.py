import sys

try:
	import RPi.GPIO as GPIO
except ImportError:
	print("Warning: could not import RPi.GPIO. Faking it!")

	class GPIOFake:
		OUT = 0
		BCM = 0
		HIGH = 0
		LOW = 0
		def setmode(self, mode):
			pass
		def setup(self, pin, mode):
			pass
		def output(self, pin, level):
			pass
		def cleanup(self):
			pass

	GPIO = GPIOFake()

LED_PIN = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def control(enable):
	if enable:
		GPIO.output(LED_PIN, GPIO.HIGH)
	else:
		GPIO.output(LED_PIN, GPIO.LOW)

if __name__ == "__main__":
	if sys.argv[1] == "on":
		control(True)
	elif sys.argv[1] == "off":
		control(False)

	try:
		while True:
			pass
	finally:
		GPIO.cleanup()

