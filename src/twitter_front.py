import tweepy
import os
import logging

class TwitterFront(tweepy.Stream):
    HANDLES_TO_FOLLOW = ['ryancohen', 'GameStop', 'GMEdd']
    LOG = logging.getLogger(__name__)

    def __init__(self, consume, test=False):
        self.LOG.debug("Logging into twitter..")

        consumer_key = os.environ["twitter_api_key"]
        consumer_secret = os.environ["twitter_api_secret"]
        access_token = os.environ["twitter_api_access_token"]
        access_token_secret = os.environ["twitter_api_access_token_secret"]

        tweepy.Stream.__init__(self, consumer_key, consumer_secret, access_token, access_token_secret)
        self.LOG.info("Logged in!")

        bearer_token = os.environ["twitter_api_bearer_token"]
        client = tweepy.Client(bearer_token)
        self.user_ids_to_follow = list(
            map(lambda handle: client.get_user(username=handle).data.id,
                self.HANDLES_TO_FOLLOW))

        self.LOG.info(f"These are the handles we're following: {self.HANDLES_TO_FOLLOW}")
        self.LOG.info(f"And these are their IDs: {self.user_ids_to_follow}")

        self.consume = consume
        self.test = test

    # Inherited from tweepy.Stream
    def on_status(self, tweet):
        if not tweet.author.screen_name in self.HANDLES_TO_FOLLOW:
            self.LOG.info(f"Ignoring tweet from author: {tweet.author.screen_name}")
            return

        url=f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
        data = {
            'url': url,
            'name': tweet.user.name
        }
        self.consume(data)

    def stream(self):
        if (self.test):
            self.filter(track="Twitter")
        else:
            self.filter(follow=self.user_ids_to_follow)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    twitter_front = TwitterFront(lambda x: logging.info(f"new tweet {x}"), test=False)
    twitter_front.stream()
