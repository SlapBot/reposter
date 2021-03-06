import os
import json


class InformationParser:
    def __init__(self, name="information.json"):
        self.filename = self.retrieve_filename(name)
        self.json_data = self.get_json_data()
        self.jobs = []
        self.place_jobs(self.json_data)

    @staticmethod
    def retrieve_filename(name):
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.pardir, os.pardir, name))
        return filename

    def get_json_data(self):
        with open(self.filename, "r") as j:
            json_data = json.load(j)
        return json_data

    def write_json_data(self, data):
        with open(self.filename, "w") as j:
            json.dump(data, j, indent=4)
        self.json_data = self.get_json_data()
        return True

    def place_jobs(self, json_data):
        for data in json_data['leads']:
            self.jobs.append(Job(data))


class Facebook:
    def __init__(self, data):
        self.page_id = data['page_id']
        self.name = data['name']
        self.token = data['token']
        self.message = data['message']


class Subreddit:
    def __init__(self, data):
        self.name = data['name']


class Job:
    def __init__(self, data):
        self.facebook = Facebook(data['facebook'])
        self.subreddits = []
        self.process_subreddits(data['subreddits'])

    def process_subreddits(self, subreddits):
        for subreddit in subreddits:
            self.subreddits.append(Subreddit(subreddit))


infoparser = InformationParser()
