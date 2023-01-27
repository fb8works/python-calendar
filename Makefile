SHELL := /bin/bash

# parameters

STYLE ?= default
CSS ?= calendar.css

# constants

SYUKUJITSU_CSV := syukujitsu.csv
OUTPUT := calendar.html
CLEANS := $(OUTPUT) $(CSS)


all: calendar watch

prep:
	@[ -e "$$(poetry env info -p)" ] || poetry install

$(OUTPUT): prep
	poetry run pycal --no-browser --output "$@" --style "$(STYLE)" --css "$(CSS)" --force

calendar: clean $(OUTPUT)

watch: PORT := $(shell python -c "import socket; s = socket.socket(); s.bind(('', 0));print(s.getsockname()[1]);s.close()")
watch: $(OUTPUT)
	(sleep 1; python -c 'import webbrowser; webbrowser.open("http://127.0.0.1:$(PORT)/$(OUTPUT)")') &
	livereload -p $(PORT)

test:
	poetry run isort .
	poetry run black .
	poetry run pflake8 .
	poetry run mypy .
	poetry run pytest

test-verify: $(SYUKUJITSU_CSV) | prep
	poetry run python -m python_calendar.test.verify

setup: prep

setup-devel:
	sudo apt-get update
	ln -srf devel/.tool-versions .
	sudo apt-get install tk-dev
	ln -srf devel/.envrc .
	direnv allow
	poetry install

clean:
	$(RM) $(CLEANS)

distclean: clean

$(SYUKUJITSU_CSV):
	poetry run python -c 'import sys, urllib.request'$$'\n''with open(sys.argv[2], mode="wb") as f: f.write(urllib.request.urlopen(sys.argv[1]).read())' "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv" "$@"

.PHONY: all prep calendar watch test test-verify setup setup-devel
