import praw
from Reposter.RedditFacebook.core.subreddit import SubReddit
from Reposter.utils.configurer import config


class PostGetter:
    def __init__(self, name):
        self.config = config
        self.reddit = praw.Reddit(
            client_id=self.config.get_configuration("client_id"),
            client_secret=self.config.get_configuration("client_secret"),
            username=self.config.get_configuration("username"),
            password=self.config.get_configuration("password"),
            user_agent=self.config.get_configuration("user_agent")
        )
        self.subreddit = SubReddit(self.reddit, name)
        self.posts = self.subreddit.get_posts()

    def get_post(self, content):
        for post in self.posts:
            if post.type == content:
                return post
        return False

    def get_posts(self):
        return self.subreddit.get_posts()

    def get_photo_post(self):
        return self.get_post(content="photo")

    def get_gif_post(self):
        return self.get_post(content="gif")

    def get_any_post(self):
        if len(self.posts) > 0:
            return self.posts[0]
            # Write your logic to get a specific post - say the most controversial? Highest Reception? Most upvotes?
        return False

