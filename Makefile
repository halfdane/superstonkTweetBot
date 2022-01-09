SHELL := /bin/bash

PROJECT=superstonkTweetBot
RASPI_USER=pi@redditbot

.PHONY: fake_run
fake_run: venv
	source .envrc && ./venv/bin/python -u src/main.py -t

.PHONY: run
run: venv
	source .envrc && ./venv/bin/python -u src/main.py

.PHONY: ssh_deploy
ssh_deploy:
	ssh -t $(RASPI_USER) '\
	cd $(PROJECT) && \
	git pull --rebase && \
	sudo systemctl restart $(PROJECT).service'

.PHONY: ssh_logs
ssh_logs:
	ssh -t $(RASPI_USER) 'journalctl -u $(PROJECT).service -f'

.PHONY: log_server
log_server:
	$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: ssh_install
ssh_install:
	ssh -t $(RASPI_USER) 'git clone https://github.com/halfdane/$(PROJECT).git'
	scp .envrc $(RASPI_USER):~/$(PROJECT)
	ssh -t $(RASPI_USER) '\
	cd $(PROJECT) && \
	sudo cp $(PROJECT).service /lib/systemd/system/ && \
	sudo systemctl daemon-reload && \
	sudo systemctl restart $(PROJECT).service'

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

.PHONY: clean
clean:
	rm -rf venv
	find -iname "*.pyc" -delete
