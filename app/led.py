import sys

import RPi.GPIO as GPIO

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

