SHELL := /bin/bash
SYUKUJITSU_CSV := syukujitsu.csv
CLEANS := calendar.html test.calendar.2023.html


all: calendar

calendar:
	poetry run python -m python_calendar.calendar

test:
	LC_ALL=C poetry run python -m python_calendar.calendar --filename test.calendar.2023.html
	diff calendar.2023.html test.calendar.2023.html

test-verify: $(SYUKUJITSU_CSV)
	poetry run python -m python_calendar.test.verify

clean:
	$(RM) $(CLEANS)

$(SYUKUJITSU_CSV):
	poetry run python -c 'import sys, urllib.request'$$'\n''with open(sys.argv[2], mode="wb") as f: f.write(urllib.request.urlopen(sys.argv[1]).read())' "https://www8.cao.go.jp/chosei/shukujitsu/syukujitsu.csv" "$@"
