SHELL := /bin/bash

.PHONY: fake_run
fake_run: venv
	./venv/bin/python src/main.py -t

.PHONY: run
run: venv
	source .envrc && ./venv/bin/python -u src/main.py

ssh_deploy:
	ssh -t pi@redditbot 'cd superstonkTweetBot && make deploy'

deploy: install
	echo "Updating codebase"
	echo git pull --rebase
	sudo systemctl restart superstonkTweetBot.service
	sleep 5
	systemctl status superstonkTweetBot.service --no-pager

install: /lib/systemd/system/superstonkTweetBot.service
	sudo cp superstonkTweetBot.service /lib/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl start test.service


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
