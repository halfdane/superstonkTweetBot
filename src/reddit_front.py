import praw
import os
import logging
from datetime import datetime

class RedditFront:

    def __init__(self, test=False):
        user_agent = "desktop:com.halfdane.diamanten_bot:v0.0.1 (by u/half_dane)"
        logging.debug("Logging in..")
        try:
            self.reddit = praw.Reddit(username=os.environ["reddit_username"],
                            password=os.environ["reddit_password"],
                            client_id=os.environ["client_id"],
                            client_secret=os.environ["client_secret"],
                            user_agent=user_agent)

            logging.info("Logged in!")
        except Exception as e:
            logging.error("Failed to log in!")
        self.test = test

    def post_superstonk_daily(self, message):
        subreddit = self.reddit.subreddit("Superstonk")
        expectedName = "$GME Daily Discussion Thread"
        for submission in subreddit.hot(limit=10):
            if (submission.title == expectedName):
                if not self.test:
                    logging.info("Commenting to https://www.reddit.com%s" % submission.permalink)
                    submission.reply(message)

    def find_diamantenhaende_post(self):
        parsnip = self.reddit.redditor("parsnip")
        for i in parsnip.submissions.new(limit=1):
            link = "https://www.reddit.com%s" % i.permalink
            
            logging.info("  %s [created (UTC) %s]" % (i.title, datetime.utcfromtimestamp(i.created_utc)))
            return link


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    reddit_front = RedditFront()
    reddit_front.find_diamantenhaende_post()
