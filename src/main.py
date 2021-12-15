import sys, getopt, os
import logging
import threading

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

    redditFront = RedditFront(test=test)
    def handle_message(data):
        message_thread = threading.Thread(target=redditFront.create_tweet_post, args=[data])
        message_thread.start()


    twitter_front = TwitterFront(handle_message, test=test)
    twitter_front.stream()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
