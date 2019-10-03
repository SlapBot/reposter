# REPOSTER

A framework to manage, monitor and deploy marketing in social-media by re-posting content from one place to the another.

![](https://github.com/SlapBot/reposter/master/screenshots/0.gif)

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

### Application Setup

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
    - Next add in your credentials after creating a page at facebook.
        - You don't need to add `long_token` that will be done by a script below.
    - Run `python facebook_perm_token.py` to get a permanent token which will be printed on the screen. Save it as we'll use it later on.
3. Write the workflow logic in declarative syntax of json at `information.json` as follows:
    - There is already an example to showcase the working.
    - `facebook` tag encapsulates all of the information needed for Facebook workflow.
        - `Name`: Name of the facebook page.
        - `page_id`: ID of the facebook page.
        - `token`: *The token retrieved from the `facebook_perm_token.py` result above.
        - `message`: If you'd wanna write the message retrieved from the posts (from Reddit or any other content aggregator).
    - `subreddits` tag allows you to mention the subreddits from where you'd wanna retrieve the posts from.
4. Now you must be able to run `python index.py` to automate the process of re-posting from one social media handle to another.

#### Periodic Posting

1. Use a crontab to schedule your posts: `crontab -e`
2. Add this entry `0 */3 * * * /<path-to-repository>/reposter/reposter-env/bin/python /<path-to-repository>/reposter/index.py >/dev/null 2>&1`
3. The above added entry creates Facebook posts every 3 hours retrieved from Reddit.


#### Advanced Setup

1. Throughout the code you can abstract a lot of entries to the `information.json` like which posts to choose from Reddit (currently its the top rated one.)
2. Adding new social media handles for retrieval and submission is super easy:
    - Create their own module and add the hooks at `information.json`
    - Regulate their separate logic in a much more modular way.

## Why?

Its one of the first pieces of software I wrote (back in 2017) when I was introduced to Python and wanted to manage social media of one of my
Open Source Project - [Stephanie](github.com/slapbot/stephanie-va) which was programmed to make automated posts in its
Facebook Page at [Stephanie - Facebook Page](https://www.facebook.com/Stephanie.VA17/).

More Pages using the program:

1. [Earthian](https://www.facebook.com/Earthian-1855714958090094/)
2. [Otterance](https://www.facebook.com/Otterance-264385350745645/)

So in the process of checking out my previous project - I just thought to make it open-source for anyone to use.

Its super simply and doesn't require any fancy programming to get started with.
