import sys, getopt, os
import logging

from twitter_front import TwitterFront
from reddit_front import RedditFront

def main(argv):
    test = False
    try:
        opts, args = getopt.getopt(argv, "t")
    except getopt.GetoptError:
        logging.error('main.py [-t testrun]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-t':
            test = True

    redditFront = RedditFront(test=test)
    def handle_message(data):
        redditFront.create_tweet_post(data)

    twitter_front = TwitterFront(handle_message, test=test)
    twitter_front.stream()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
