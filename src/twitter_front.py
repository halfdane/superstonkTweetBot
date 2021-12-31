import tweepy
import os
import logging

import pytz

from test_only_exception import TestOnlyException

nyse = pytz.timezone('US/Eastern')


class TwitterFront(tweepy.Stream):
    LOG = logging.getLogger(__name__)

    def __init__(self, consume, test=False):
        self.LOG.debug("Logging into twitter..")

        consumer_key = os.environ["twitter_api_key"]
        consumer_secret = os.environ["twitter_api_secret"]
        access_token = os.environ["twitter_api_access_token"]
        access_token_secret = os.environ["twitter_api_access_token_secret"]

        self.twitter_handles_to_follow = os.environ["twitter_handles_to_follow"].split()

        tweepy.Stream.__init__(self, consumer_key, consumer_secret, access_token, access_token_secret)
        self.LOG.info("Logged in!")

        bearer_token = os.environ["twitter_api_bearer_token"]
        client = tweepy.Client(bearer_token)
        self.user_ids_to_follow = list(
            map(lambda handle: client.get_user(username=handle).data.id,
                self.twitter_handles_to_follow))

        self.LOG.info(f"These are the handles we're following: {self.twitter_handles_to_follow}")
        self.LOG.info(f"And these are their IDs: {self.user_ids_to_follow}")

        self.consume = consume
        self.test = test

    # Inherited from tweepy.Stream
    def on_status(self, tweet):
        if (not tweet.author.screen_name in self.twitter_handles_to_follow) and (not self.test):
            self.LOG.info(f"Ignoring tweet from author: {tweet.author.screen_name}")
            return

        url = f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
        data = {
            'url': url,
            'screen_name': tweet.user.screen_name,
            'created_at': tweet.created_at.astimezone(nyse),
            'tweet_id': tweet.id
        }
        self.LOG.info(f"consuming {data}")
        self.consume(data)

        if self.test:
            raise TestOnlyException

    def stream(self):
        if self.test:
            self.filter(track="Twitter")
        else:
            self.filter(follow=self.user_ids_to_follow, threaded=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    twitter_front = TwitterFront(lambda x: logging.info(f"new tweet {x}"), test=True)
    twitter_front.stream()
