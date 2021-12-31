import requests
import logging
import os

class ScreenshotFront:
    LOG = logging.getLogger(__name__)

    def __init__(self, test=False):
        self.test = test

    def take_screenshot(self, handle, tweet_id):
        output_file=f"screenshot_{handle}_{tweet_id}.png"

        self.LOG.info(f"Taking screenshot of {handle} {tweet_id}")
        r = requests.get(f"https://tweets-as-an-image.herokuapp.com/tweet?twitterHandle={handle}&id={tweet_id}")
        with open(output_file, 'wb') as f:
            f.write(r.content)
        return output_file

    def cleanup_screenshot(self, screenshot_file):
        os.remove(screenshot_file)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    screenshot_front = ScreenshotFront()
    output = screenshot_front.take_screenshot("GameStop", "1470793223962517512")
