import sys, getopt, os
import logging

from twitter_front import TwitterFront

def handle_message(data):
    logging.info(f"new tweet from {data['name']}: {data['url']} ")

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

    twitter_front = TwitterFront(handle_message, test=test)
    twitter_front.stream()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main(sys.argv[1:])
