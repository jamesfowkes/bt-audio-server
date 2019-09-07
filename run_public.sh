python3 run.py public /home/pi/cave-escape-projector/projector.log &
python3 card_reader_app.py /dev/ttyUSB0 http://0.0.0.0:8888/api/rfid/scan &
