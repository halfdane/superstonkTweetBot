import tweepy
import os
import logging

class TwitterFront(tweepy.Stream):
    HANDLES_TO_FOLLOW = ['ryancohen', 'GameStop', 'GMEdd']

    def on_status(self, tweet):
        url=f"https://twitter.com/{tweet.user.screen_name}/status/{tweet.id}"
        data = {
            'url': url,
            'name': tweet.user.name
        }
        self.consume(data)

    def __init__(self, consume, test=False):
        logging.debug("Logging into twitter..")
        try:
            consumer_key = os.environ["twitter_api_key"]
            consumer_secret = os.environ["twitter_api_secret"]
            access_token = os.environ["twitter_api_access_token"]
            access_token_secret = os.environ["twitter_api_access_token_secret"]
            bearer_token = os.environ["twitter_api_bearer_token"]

            client = tweepy.Client(bearer_token)
            self.user_ids_to_follow = list(
                map(lambda handle: client.get_user(username=handle).data.id,
                    self.HANDLES_TO_FOLLOW))

            tweepy.Stream.__init__(self, consumer_key, consumer_secret, access_token, access_token_secret)

            self.consume = consume
            self.test = test

            logging.info("Logged in!")
        except Exception as e:
            logging.error("Failed to log in!", e)

    def stream(self):
        if (self.test):
            self.filter(track="Twitter")
        else:
            self.filter(follow=self.user_ids_to_follow)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    twitter_front = TwitterFront(lambda x: logging.info(f"new tweet from {x['name']}: {x['url']} "), test=True)
    twitter_front.stream()
