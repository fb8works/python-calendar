SHELL := /bin/bash

# parameters

CSS ?= calendar.css

# constants

SYUKUJITSU_CSV := syukujitsu.csv
OUTPUT := calendar.html

TEST_YEAR := 2023
OUTPUT_SAMPLE := calendar.$(TEST_YEAR).sample.html
OUTPUT_TEST := calendar.$(TEST_YEAR).html

CLEANS := $(OUTPUT) $(OUTPUT_TEST)


all: calendar watch

prep:
	@[ -e "$$(poetry env info -p)" ] || poetry install

$(OUTPUT): prep
	poetry run python -m python_calendar.calendar --output $@ --css "$(CSS)"

$(OUTPUT_TEST): prep
	LC_ALL=C poetry run python -m python_calendar.calendar --css "calendar-simple.css" --year $(TEST_YEAR) --output "$@"

calendar: clean $(OUTPUT)

watch: $(OUTPUT)
	$ (sleep 1; wslstart http://127.0.0.1:8888/$(OUTPUT) &); livereload -p 8888

test: $(OUTPUT_SAMPLE) $(OUTPUT_TEST) 
	diff $^

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
