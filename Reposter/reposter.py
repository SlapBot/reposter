from Reposter.RedditFacebook.post_getter import PostGetter
from Reposter.FacebookReddit.post_submitter import PostSubmitter
from Reposter.utils.information_parser import infoparser


class Reposter:
    def __init__(self):
        self.infoparser = infoparser

    def main(self):
        for job in self.infoparser.jobs:
            try:
                self.execute(job)
            except Exception:
                pass

    def execute(self, job, tries=0, max_tries=5):
        posts = self.get_posts(job.subreddits)
        tries += 1
        if not posts and tries < max_tries:
            return self.execute(job, tries)
        else:
            self.submit_posts(job.facebook, posts)

    @staticmethod
    def get_posts(subreddits):
        posts = []
        for subreddit in subreddits:
            pg = PostGetter(subreddit.name)
            post = pg.get_any_post()
            print("Got my post as %s from %s subreddit." % (post.url, subreddit.name))
            posts.append(post)
        return posts

    @staticmethod
    def submit_posts(social_media, posts):
        ps = PostSubmitter(social_media.page_id, social_media.token, social_media.message)
        for post in posts:
            ps.submit_post(post)
            print("Posted my post as %s for %s page." % (post.title, social_media.name))
