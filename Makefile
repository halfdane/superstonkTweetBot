SHELL := /bin/bash

.PHONY: fake_run
fake_run: venv
	./venv/bin/python src/main.py -t

.PHONY: run
run: venv
	./venv/bin/python src/main.py

ssh_screen:
	echo "Exit with CTRL-a d"
	ssh -t pi@redditbot screen -R superstonkTweetBot

ssh_deploy:
	ssh -t pi@redditbot 'cd superstonkTweetBot && make deploy'

deploy:
	echo "Updating codebase"
	git pull --rebase
	echo "Killing running screen session"
	screen -ls "superstonkTweetBot" && screen -S superstonkTweetBot -p 0 -X quit || echo "Nothing to kill"
	echo "Starting new session within screen"
	screen -dmS superstonkTweetBot make run
	echo "That's all folks"


venv: venv/touchfile

venv/touchfile: requirements.txt
	echo "###########################################"
	echo "Setting up virtualenv with dependencies..."
	echo "###########################################"
	echo $(shell which python3)
	python3 -m virtualenv -p $(shell which python3) venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r "requirements.txt"
	touch venv/touchfile

clean:
	rm -rf venv
	find -iname "*.pyc" -delete
