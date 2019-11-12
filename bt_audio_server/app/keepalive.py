import threading
import time
import pathlib

from app.media import play_audio

class KeepAliveThread(threading.Thread):

    def __init__(self, media_folder):
        super(KeepAliveThread, self).__init__()
        self.run_flag = True
        self.media_folder = media_folder

    def run(self):

        while self.run_flag:
        	audio_path = pathlib.Path(self.media_folder, "keepalive.mp3")
        	play_audio(audio_path)
        	time.sleep(60*10.0)

    def stop_thread(self):
        self.run_flag = False