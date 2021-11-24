import praw
import os
import logging

class RedditFront:
    LOG = logging.getLogger(__name__)

    def __init__(self, test=False):
        user_agent = "desktop:com.halfdane.superstonk_tweet_bot:v0.0.1 (by u/half_dane)"
        self.LOG.debug("Logging in..")

        self.reddit = praw.Reddit(username=os.environ["reddit_username"],
                        password=os.environ["reddit_password"],
                        client_id=os.environ["reddit_client_id"],
                        client_secret=os.environ["reddit_client_secret"],
                        user_agent=user_agent)
        self.LOG.info(f"Logged in as {self.reddit.user.me()}")

        self.reddit.validate_on_submit = True
        self.subreddit = self.reddit.subreddit(os.environ["target_subreddit"])
        self.LOG.info(f'submitting to {self.subreddit.display_name}')

        for flair in self.subreddit.flair.link_templates:
            if ("Social Media" in flair['text']):
                self.flair = flair

        if (not hasattr(self, 'flair')):
            raise Exception("Couldn't find a fitting flair! Aborting now.")

        self.LOG.info(f"Using the flair {self.flair['text']} for submissions")

        self.test = test

    def create_tweet_post(self, data):
        title=f"New Tweet from {data['name']}",
        url=data['url']
        flair_id=self.flair['id']

        self.LOG.info(f"""Submitting new post:
            title: {title}
            url: {url}
        """)
        if (not self.test):
            self.subreddit.submit(title=title, url=url, flair_id=flair_id)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reddit_front = RedditFront(test=False)
    reddit_front.create_tweet_post({'url': "128.0.0.1", 'name': "halfdane"})
