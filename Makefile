SHELL := /bin/bash

# parameters

STYLE ?= default
CSS ?= calendar.css

# constants

SYUKUJITSU_CSV := syukujitsu.csv
OUTPUT := calendar.html
CLEANS := $(OUTPUT) $(CSS)
PACKAGE := python_calendar


all: calendar watch

setup: prep

prep:
	@[ -e "$$(poetry env info -p)" ] || poetry install

setup-devel:
	cp devel/.tool-versions .
	cp devel/.envrc .

$(OUTPUT): prep
	poetry run pycal --no-browser --output "$@" --style "$(STYLE)" --css "$(CSS)" --force

calendar: clean $(OUTPUT)

watch: PORT := $(shell poetry run python -c "import socket; s = socket.socket(); s.bind(('', 0));print(s.getsockname()[1]);s.close()")
watch: $(OUTPUT)
	(sleep 1; poetry run python -c 'import webbrowser; webbrowser.open("http://127.0.0.1:$(PORT)/$(OUTPUT)")') &
	poetry run livereload -p $(PORT)

lint:
	poetry run isort .
	poetry run black .
	poetry run mypy .

test:
	poetry run pytest

test-verify: $(SYUKUJITSU_CSV) | prep
	poetry run python -m $(PACKAGE).test.verify

pre-commit: lint setup.py requirements.txt

setup.py: pyproject.toml poetry.lock README.md
	rm -rf dist
	poetry build
	tar xzf dist/$(PACKAGE)-*.tar.gz -C ./dist
	cp dist/$(PACKAGE)-*/setup.py setup.py.temp
	sed -i -e 's/^\(setup(\*\*setup_kwargs)\)$$/\1  # type: ignore/' setup.py.temp
	mv setup.py.temp setup.py
	rm -rf dist

requirements.txt: pyproject.toml poetry.lock
	poetry export --format=requirements.txt --output=$@ --without-hashes

clean:
	$(RM) $(CLEANS)

distclean: clean

$(SYUKUJITSU_CSV):
	poetry run python -c $$'import sys, urllib.request\ncontent = urllib.request.urlopen(sys.argv[1]).read()\nwith open(sys.argv[2], mode="wb") as f: f.write(content)' "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv" "$@"

.PHONY: all prep setup setup-devel calendar watch lint test test-verify clean distclean
