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

    if test:
        logging.info("Running in test mode")

    reddit_front = RedditFront(test=test)
    twitter_front = TwitterFront(reddit_front.create_tweet_post, test=test)
    twitter_front.stream()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
