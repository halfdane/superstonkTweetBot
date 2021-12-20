SHELL := /bin/bash

PROJECT=superstonkTweetBot
RASPI_USER=pi@redditbot

.PHONY: log_server
log_server:
	websocketd --staticdir=. --port 1234 journalctl -u $(PROJECT) -f &
