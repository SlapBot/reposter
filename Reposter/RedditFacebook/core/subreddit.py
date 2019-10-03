from Reposter.RedditFacebook.core.post import Post
from Reposter.utils.logger import logger
from Reposter.utils.configurer import config


class SubReddit:
    def __init__(self, reddit, name):
        self.reddit = reddit
        self.config = config
        self.logger = logger
        self.subreddit = self.reddit.subreddit(name)
        self.allowed_domains = self.parse_allowed_domains()
        self.repost_ids = self.logger.ids

    def parse_allowed_domains(self):
        return self.config.get_configuration("allowed_domains").split(" ")

    def retrieve_submissions(self, limit=10):
        submissions = []
        for submission in self.subreddit.hot(limit=limit):
            if submission.id not in self.repost_ids:
                if submission.domain in self.allowed_domains:
                    submissions.append(submission)
        return submissions

    def retrieve_posts(self, submissions):
        posts = []
        for submission in submissions:
            posts.append(Post(post_id=submission.id, title=submission.title, url=submission.url,
                              type=self.guess_type(submission.url)))
        return posts

    def get_posts(self):
        submissions = self.retrieve_submissions()
        posts = self.retrieve_posts(submissions)
        return posts

    @staticmethod
    def guess_type(url):
        if url[len(url) - 4:] == "gifv":
            return "gif"
        else:
            "photo"
