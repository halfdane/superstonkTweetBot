import os
import requests
import logging

class ScreenshotFront:
    def __init__(self, test=False):
        self.test = test

        self.tweetpik_api_key = os.environ["tweetpik_api_key"]

    def take_screenshot(self, tweetId):
        r = requests.post('https://tweetpik.com/api/images',
            data="{\"tweetId\": \"%s\"}" % tweetId,
            headers={'Authorization': self.tweetpik_api_key, "Content-Type": "application/json"})

        print(r.json()['url'])

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    screenshot_front = ScreenshotFront(test=False)
    screenshot_front.take_screenshot("1463764408996409347")
