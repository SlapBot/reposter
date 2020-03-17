# REPOSTER

A framework to manage, monitor and deploy marketing in social-media by re-posting content from one place to the another.

- [Motivation](#motivation)
- [Features](#features)
- [Installation](#installation)
    - [Pre-Requisites](#pre-requisites)
    - [Application Setup](#application-setup)
        - [Docker Setup](#docker-setup)
        - [Native Setup](#native-setup)
    - [Authentication Setup](#authentication-setup)
- [Usage](#usage)
    - [Periodic-Posting](#periodic-posting)
        - [Application Scheduling](#application-scheduling)
        - [Crontab](#crontab)
    - [Advanced Setup](#advanced-setup)
- [Why?](#why)

## Motivation

I wanted a setup that could be give me an entire control over content creation in a programmable automated way. With this framework, I can add as many as content retrievers and submitters as possible and create any kind of dynamic programmable workflow between them.

So for example, I could have reddit -> multiple facebook pages, twitter, instagram pages content submission, or tumblr, reddit, custom website -> Multiple facebook pages, twitter, etc. without really worrying about the underlying integration part.

Consider it like a free zapier across social media handle content management.

![](https://github.com/SlapBot/reposter/blob/master/screenshots/0.gif)

## Features

1. Declarative setup to control the submission of re-posts.
2. Out of the box support for Reddit -> Facebook re-posts.
3. Super simple API to add new social media handles for retrieval or submission of content.
4. Super clean logging with logic to ensure duplicate posts don't get posted.
5. Add support of many-to-many reposts for as many handles, pages you want.
    - Like Reddit -> Facebook, Instagram, Twitter.
    - Like Tumblr -> Facebook, Reddit, HackerNews.
    - Reddit (multiple subreddits), Tumblr -> Facebook (Multiple Pages), Twiiter (Multiple Handles)
6. Remember its just the boilerplate allowing you to come up with any kind of imagination of its use-cases and social media handles.


## Installation

### Pre-requisites

1. Python3
2. pip
3. virtualenv

### Application Setup

#### Docker Setup
1. Run `docker-compose build` to build the docker-image.
- Additional notes: 
    - To run: `docker-compose up` after you're done with the authentication setup.
    - By default it runs an application scheduler: [Application Scheduling](#application-scheduling)
    - You can make it run regular index setup by swapping line `CMD [ "python", "./schedule_index.py" ]` in `Dockerfile-reposter` with `CMD [ "python", "./index.py" ]`
#### Native Setup
1. Clone the repository: `git clone github.com/slapbot/reposter`
2. Cd into the directory: `cd reposter`
3. Create a virtualenv for python: `python -m venv reposter-env`
4. Activate the virtualenv:
    - Linux: `source reposter-env/bin/activate`
    - Windows: `source reposter-env/Scripts/activate`
5. Upgrade your pip to latest version: `pip install --upgrade pip`
6. Install the application level dependencies: `pip install -r requirements.txt`

### Authentication Setup

1. Create a Reddit bot and add in the credentials at: config.ini under `[REDDIT]` section.
    - `allowed_domain`: Enter the domains that you want to parse for content retrieval.
2. Add in your page information at `config.ini` as a section like `[STEPHANIE]` shown in the example.
    - Next add in your credentials after creating an app at facebook.
        - Fill in the `app_id` and `app_secret` from facebook console.
        - Fill in the `short_token` which will act as user-access-token from [Graph API Console](https://developers.facebook.com/tools/explorer)
            - Ensure that you give it these permissions
                ```user_birthday
                email
                manage_pages
                pages_manage_cta
                pages_show_list
                publish_pages
                publish_to_groups
                public_profile
              ```
3. Write the workflow logic in declarative syntax of json at `information.json` as follows:
    - There is already an example to showcase the working.
    - `facebook` tag encapsulates all of the information needed for Facebook workflow.
        - `Name`: Name of the facebook page.
        - `page_id`: ID of the facebook page.
        - `token`: leave it blank for now.
        - `message`: If you'd wanna write the message retrieved from the posts (from Reddit or any other content aggregator).
    - `subreddits` tag allows you to mention the subreddits from where you'd wanna retrieve the posts from.
4. Run `python facebook_perm_token.py` to get a permanent page access tokens for each page which will automatically be inserted
in `informations.json` file.
5. Now you must be able to run `python index.py` to automate the process of re-posting from one social media handle to another.

## Usage
```
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

```
### Periodic Posting

#### Application Scheduling
1. Go to `schedule_index.py` and add commands like:
    - `schedule.every(3).hours.do(run, r)` to run every 3 hours.
    - `schedule.every(70).mins.do(run, r)` to run every 70 minutes.
2. Run `python schedule_index.py` instead of `index.py`
3. The default added entry creates Facebook posts every 3 hours retrieved from Reddit.

#### Crontab
1. Use a crontab to schedule your posts: `crontab -e`
2. Add this entry `0 */3 * * * /<path-to-repository>/reposter/reposter-env/bin/python /<path-to-repository>/reposter/index.py >/dev/null 2>&1`
3. The above added entry creates Facebook posts every 3 hours retrieved from Reddit.


### Advanced Setup

1. Throughout the code you can abstract a lot of entries to the `information.json` like which posts to choose from Reddit (currently its the top rated one.)
2. Adding new social media handles for retrieval and submission is super easy:
    - Create their own module and add the hooks at `information.json`
    - Regulate their separate logic in a much more modular way.

## Why?

Its one of the first pieces of software I wrote (back in 2017) when I was introduced to Python and wanted to manage social media handles of one of my
Open Source Project - [Stephanie](github.com/slapbot/stephanie-va) which was programmed to make automated posts in its
Facebook Page at [Stephanie - Facebook Page](https://www.facebook.com/Stephanie.VA17/).

More Pages using the program:

1. [Earthian](https://www.facebook.com/Earthian-1855714958090094/)
2. [Otterance](https://www.facebook.com/Otterance-264385350745645/)

So in the process of checking out my previous project - I just thought to make it open-source for anyone to use.

Its super simply and doesn't require any fancy programming to get started with.
