import requests
import facebook
from Reposter.utils.logger import logger
import urllib.request
import os


class PostSubmitter:
    def __init__(self, page_id,
                 token,
                 message=False):
        self.page_id = page_id
        self.oauth_access_token = token
        self.message = message
        self.graph = facebook.GraphAPI(self.oauth_access_token)
        self.logger = logger

    def post(self, post, content):
        status = True
        post_title = None
        if self.message:
            post_title = post.title
        try:
            if content == "photo":
                self.graph.put_object(self.page_id, "photos",
                                      message=post_title,
                                      url=post.url)
            elif content == "gif":
                self.graph.put_object(self.page_id, "videos",
                                      message=post_title,
                                      url=self.parse_gif_url(post.url))
        except Exception as e:
            print(e)
            status = False
        if status:
            self.logger.log(post)
        return status

    def post_photo(self, post):
        return self.post(post, content="photo")

    def post_gif(self, post):
        gif_url = self.parse_gif_url(post.url)
        gif_filename = self.get_gif_file(gif_url)
        self.post_to_facebook(post, gif_filename)
        os.unlink(gif_filename)

    @staticmethod
    def parse_gif_url(url):
        if url[len(url) - 4:] == "gifv":
            return url[:len(url) - 4] + "gif"
        elif url[len(url) - 3:] == "gif":
            return url[:len(url) - 3] + "gif"
        return False

    def get_gif_file(self, gif_url):
        response = urllib.request.urlopen(gif_url)
        data = response.read()  # a `bytes` object
        filename = self.save_gif_file(data)
        return filename

    @staticmethod
    def save_gif_file(data):
        filename = "tempfile.gif"
        with open(filename, 'wb') as gf:
            gf.write(data)
            gf.close()
        return filename

    def post_to_facebook(self, post, gif_filename):
        gif_file = {'file': open(gif_filename, 'rb')}
        url = 'https://graph-video.facebook.com/%s/videos?access_token=%s' % (self.page_id, self.oauth_access_token)
        response = requests.post(url, files=gif_file)
        print(response.text)
        self.logger.log(post)

    def submit_post(self, post):
        if post.type == "gif":
            self.post_gif(post)
        else:
            self.post_photo(post)
