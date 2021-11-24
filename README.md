# diamantenbot

a reddit bot that fetches the prices of $GME in tradegate (in €) and calculates it to USD using the current conversion rate.
That information is then posted into the daily thread of superstonk.

Passing the parameter '-t' enables the test-mode which doesn't actually creates a reddit comment.


# Run

You have to export the following environment variables:
 
    export client_id="some-client-id"
    export client_secret="random gibberish"
    export reddit_username="half_dane"
    export reddit_password="very_secret"

Afterwards execute

    make

This sets up the venv for python and downloads the necessary dependencies before running the bot in test-mode 

# Targets

    make fake_run   # execute the bot in test mode.
    make run        # execute the bot in normal mode. Please note that this will create a new comment with each execution
    make clean      # clean up compile results and the venv
