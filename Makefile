SHELL := /bin/bash

.PHONY: fake_run
fake_run: venv
	source .envrc && ./venv/bin/python -u src/main.py -t

.PHONY: run
run: venv
	source .envrc && ./venv/bin/python -u src/main.py

ssh_deploy:
	ssh -t pi@redditbot '\
	cd superstonkTweetBot && \
	echo git pull --rebase && \
	sudo systemctl restart superstonkTweetBot.service && \
	sleep 5 && \
	systemctl status superstonkTweetBot.service --no-pager'

ssh_install:
	ssh -t pi@redditbot 'git clone https://github.com/halfdane/superstonkTweetBot.git'
	scp .envrc pi@redditbot:~/superstonkTweetBot
	ssh -t pi@redditbot '\
	cd superstonkTweetBot && \
	sudo cp superstonkTweetBot.service /lib/systemd/system/ && \
	sudo systemctl daemon-reload && \
	sudo systemctl restart superstonkTweetBot.service'

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
