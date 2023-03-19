# python-calendar

[![Python Lint & Test](https://github.com/fb8works/python-calendar/actions/workflows/python-app-custom.yml/badge.svg)](https://github.com/fb8works/python-calendar/actions/workflows/python-app-custom.yml)

Holiday calendar utility with HTML output.

祝日を含むカレンダーを表示／生成するツール。
コピーする事で excel に貼り付ける事ができます。

![screenshot](https://github.com/fb8works/python-calendar/blob/main/screenshot.png?raw=true)

## Requirements

- Python 3.8.0 or later
- elinks (OPTIONAL)

## Install

```bash
pip install git+https://github.com/fb8works/python-calendar.git
```

## Show calendar with holidays

Print a calendar for this month. requires w3m or elinks. you must install elinks if you want color.

```bash
pycal
```

## HTML calendar

Generate HTML calendar for this year.

```bash
pycal -H 2023
```

## Arguments and options

```
$ pycal --help
Usage: pycal [OPTIONS] [ARGS]...

Options:
  -t, --text                      Text mode
  -H, --html                      HTML mode
  -w, --width INTEGER RANGE       Width of columns.  [1<=x<=12]
  -m, --start-month INTEGER RANGE
                                  Start month.  [1<=x<=12]
  -d, --first-weekday [mon|tue|wed|thu|fri|sat|sun]
                                  First weekday.  [default: sun]
  -o, --output TEXT               Output HTML filename.
  -h, --holidays                  Include holiday list.
  -l, --list-holidays             List holidays.
  -c, --css TEXT                  Output css filename. (relative from output
                                  directory)
  -e, --use-external-css          Use external css file.
  --css-href TEXT                 CSS location or URL.
  -s, --style [default|simple]    CSS template name.  [default: default]
  --encoding TEXT                 Character encoding for HTML.
  --locale TEXT                   Locale eg. en_US.UTF-8.
  -C, --country TEXT              Country code for holidays. eg. US (default
                                  is same as locale)
  --subdiv TEXT                   Specify subdivision.
  --financial TEXT                Use financial holiday.
  -f, --force                     Force overwrite css file.
  -q, --quiet                     Quiet mode.
  -n, --no-browser                Do not open browser.
  -c, --color                     color mode (text mode).
  -v, --verbose                   Show information.
  --help                          Show this message and exit.
```

## Locale

You can change the calendar locale. Defaults to LC_ALL, LC_TIME, LANG environment variable or 'C'.

```bash
pycal --locale=en_US
```

## Country

You can change the region of country that determines the holiday. default is same as locale.

```bash
pycal --country=JP
```

## Subdivision

The subdivisions can be specified. eg. for california.

```bash
pycal --locale=en_US --subdiv=CA
```

## Financial holiday

If you want clendar that uses financial holidays. The --country option is ignored.

```bash
pycal --financial=NYSE
```

## Style sheet

HTML カレンダーを生成するとカレントディレクトリに calendar.css が生成されます。
スタイルシートを編集することで祝日の色等を変更する事ができます。 --inline-css オプションを指定した場合は css は生成されません。

```css
.holiday {
    background: red;
}
.day.sun {
    background: pink;
}
.day.sat {
    background: skyblue;
}
```

## NOTE

[内閣府の祝日データ](https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html) と holidays, jpholidays モジュールの相違を比較検証します。

```bash
$ make test-verify
```
