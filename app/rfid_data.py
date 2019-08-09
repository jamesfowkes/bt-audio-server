import json
import pathlib
import collections

class RFIDDataStore:

    def __init__(self, filename):
        self.filename = filename
        self.rfid_log = collections.deque(maxlen=10)

        path = pathlib.Path(self.filename)
        if not path.exists():
            with open(self.filename, "w") as fp:
                json.dump({}, fp, indent=4)        

    def load(self):
        with open(self.filename, "r") as fp:
            data = json.load(fp)
        return data

    def save(self, data):
        with open(self.filename, "w") as fp:
            json.dump(data, fp, indent=4)

    def update(self, uid, target):
        data = self.load()
        data[uid] = target
        self.save(data)

    def query(self, uid):
        data = self.load()
        return data.get(uid, None)

    def log(self, uid):
        self.rfid_log.append(uid)

    def print_log(self):
        for uid in self.rfid_log:
            print(uid)

    def get_last(self):
        try:
            return self.rfid_log[-1]
        except IndexError:
            return None

