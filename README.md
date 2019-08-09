# cave-escape-projector
A Pi/Python server for playing movies on a TFT screen

## Installation

Run `install.sh` , which will install and setup:

 - the Python webservice 
 - the LCD kernel module
 - the samba share

Add .envrc file to the root directory with
export PROJECTOR_WEBSERVER_CONFIG_PATH=<path-to-config-file>

## Pin Mapping

The RFID reader is on SPI bus 1, with CE2 (which is /dev/spidev1.2)
In addition, RST is on BCM5. CE2 is BCM16.

The LCD is on SPI bus 0, with CE0 (which is /dev/spidev0.0)
In addition, reset is on BCM23, D/C is on BCM18, LED is on BCM24.
