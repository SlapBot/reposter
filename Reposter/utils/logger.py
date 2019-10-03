import os
import json
import time


class Logger:
    def __init__(self, name="log.json"):
        self.filename = self.retrieve_filename(name)
        self.json_data = self.get_json_data(self.filename)
        self.ids = self.get_already_posted_ids(self.json_data)
        
    @staticmethod
    def retrieve_filename(name):
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.pardir, os.pardir, name))
        return filename

    @staticmethod
    def get_json_data(filename):
        with open(filename, "r") as j:
            json_data = json.load(j)
            j.close()
        return json_data

    @staticmethod
    def get_already_posted_ids(data):
        return data

    def log(self, post):
        self.ids[post.id] = {
            "title": post.title,
            "url": post.url,
            "posted_at": time.ctime()
        }

        with open(self.filename, "w") as j:
            json.dump(self.ids, j)
            j.close()
        return True

logger = Logger()
