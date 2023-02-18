# python-calendar

[![Python Lint & Test](https://github.com/fb8works/python-calendar/actions/workflows/python-app-custom.yml/badge.svg)](https://github.com/fb8works/python-calendar/actions/workflows/python-app-custom.yml)

Tool to create an anual calendar available in Excel.

シンプルな４月始まりのカレンダーを html で生成します。
コピーする事で excel に貼り付ける事ができます。

![screenshot](https://github.com/fb8works/python-calendar/blob/main/screenshot.png?raw=true)

## Requirements

- Python 3.8.0 or later

## Install

```bash
pip install git+https://github.com/fb8works/python-calendar.git
```

## Generate calendar

Generate a calendar for this year.

```bash
pycal
```

Generate a calendar for the year 2023 with the first day of the week being Sunday and starting in April.

```bash
pycal 2023 sun 4
```

## Arguments and options

```
$ pycal --help
Usage: pycal [OPTIONS] [YEAR] [[mon|tue|wed|thu|fri|sat|sun]] [START_MONTH]

Options:
  --width INTEGER RANGE         Width of columns.  [default: 3; 1<=x<=12]
  -o, --output TEXT             Output HTML filename.  [default:
                                calendar.html]
  --css TEXT                    Output css filename. (relative from output
                                directory)
  --css-href TEXT               CSS location or URL.
  -s, --style [default|simple]  CSS template name.  [default: default]
  --encoding TEXT               Character encoding for HTML.  [default: utf-8]
  --locale TEXT                 Locale eg. en_US.UTF-8.
  -c, --country TEXT            Country code for holidays. eg. US (default is
                                same as locale)
  --subdiv TEXT                 Specify subdivision.
  --financial TEXT              Use financial holiday.
  -f, --force                   Force overwrite css file.
  --no-browser                  Do not open browser.
  -v, --verbose                 Show information.
  --help                        Show this message and exit.
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

カレンダーを生成するとカレントディレクトリに calendar.css が生成されます。
スタイルシートを編集することで祝日の色等を変更する事ができます。

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

```
+------------+--------------------------+----------------------------+----------------------------------+
|    Date    |        Syukujitsu        |          Holidays          |            JPHoliday             |
+------------+--------------------------+----------------------------+----------------------------------+
| 1955-05-04 |            -             |             -              |            国民の休日            |
| 1956-05-04 |            -             |             -              |            国民の休日            |
| 1957-05-04 |            -             |             -              |            国民の休日            |
| 1959-04-10 |         結婚の儀         |          結婚の儀          |    皇太子・明仁親王の結婚の儀    |
| 1959-05-04 |            -             |             -              |            国民の休日            |
| 1960-05-04 |            -             |             -              |            国民の休日            |
| 1961-05-04 |            -             |             -              |            国民の休日            |
| 1962-05-04 |            -             |             -              |            国民の休日            |
| 1963-05-04 |            -             |             -              |            国民の休日            |
| 1964-05-04 |            -             |             -              |            国民の休日            |
| 1965-05-04 |            -             |             -              |            国民の休日            |
| 1966-05-04 |            -             |             -              |            国民の休日            |
| 1967-05-04 |            -             |             -              |            国民の休日            |
| 1968-05-04 |            -             |             -              |            国民の休日            |
| 1970-05-04 |            -             |             -              |            国民の休日            |
| 1971-05-04 |            -             |             -              |            国民の休日            |
| 1972-05-04 |            -             |             -              |            国民の休日            |
| 1973-02-12 |            -             |             -              |      建国記念の日 振替休日       |
| 1973-04-30 |           休日           |          振替休日          |       天皇誕生日 振替休日        |
| 1973-05-04 |            -             |             -              |            国民の休日            |
| 1973-09-24 |           休日           |          振替休日          |        秋分の日 振替休日         |
| 1974-05-04 |            -             |             -              |            国民の休日            |
| 1974-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |
| 1974-09-16 |           休日           |          振替休日          |        敬老の日 振替休日         |
| 1974-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |
| 1975-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |
| 1976-05-04 |            -             |             -              |            国民の休日            |
| 1976-10-11 |           休日           |          振替休日          |        体育の日 振替休日         |
| 1977-05-04 |            -             |             -              |            国民の休日            |
| 1978-01-02 |           休日           |          振替休日          |          元日 振替休日           |
| 1978-01-16 |           休日           |          振替休日          |        成人の日 振替休日         |
| 1978-05-04 |            -             |             -              |            国民の休日            |
| 1979-02-12 |           休日           |          振替休日          |      建国記念の日 振替休日       |
| 1979-04-30 |           休日           |          振替休日          |       天皇誕生日 振替休日        |
| 1979-05-04 |            -             |             -              |            国民の休日            |
| 1980-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |
| 1981-05-04 |           休日           |          振替休日          |       憲法記念日 振替休日        |
| 1982-03-22 |           休日           |          振替休日          |        春分の日 振替休日         |
| 1982-05-04 |            -             |             -              |            国民の休日            |
| 1982-10-11 |           休日           |          振替休日          |        体育の日 振替休日         |
| 1983-05-04 |            -             |             -              |            国民の休日            |
| 1984-01-02 |           休日           |          振替休日          |          元日 振替休日           |
| 1984-01-16 |           休日           |          振替休日          |        成人の日 振替休日         |
| 1984-04-30 |           休日           |          振替休日          |       天皇誕生日 振替休日        |
| 1984-05-04 |            -             |             -              |            国民の休日            |
| 1984-09-24 |           休日           |          振替休日          |        秋分の日 振替休日         |
| 1985-05-04 |            -             |             -              |            国民の休日            |
| 1985-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |
| 1985-09-16 |           休日           |          振替休日          |        敬老の日 振替休日         |
| 1985-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |
| 1986-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |
| 1987-05-04 |           休日           |          振替休日          |       憲法記念日 振替休日        |
| 1988-03-21 |           休日           |          振替休日          |        春分の日 振替休日         |
| 1988-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 1988-12-23 |            -             |             -              |            天皇誕生日            |
| 1989-01-02 |           休日           |          振替休日          |          元日 振替休日           |
| 1989-01-16 |           休日           |          振替休日          |        成人の日 振替休日         |
| 1989-02-24 |         大喪の礼         |          大喪の礼          |        昭和天皇の大喪の礼        |
| 1989-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 1990-02-12 |           休日           |          振替休日          |      建国記念の日 振替休日       |
| 1990-04-30 |           休日           |          振替休日          |       みどりの日 振替休日        |
| 1990-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 1990-09-24 |           休日           |          振替休日          |        秋分の日 振替休日         |
| 1990-11-12 |      即位礼正殿の儀      |       即位礼正殿の儀       |         即位の礼正殿の儀         |
| 1990-12-24 |           休日           |          振替休日          |       天皇誕生日 振替休日        |
| 1991-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 1991-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |
| 1991-09-16 |           休日           |          振替休日          |        敬老の日 振替休日         |
| 1991-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |
| 1992-05-04 |           休日           |          振替休日          |       憲法記念日 振替休日        |
| 1993-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 1993-06-09 |         結婚の儀         |          結婚の儀          | 皇太子・皇太子徳仁親王の結婚の儀 |
| 1993-10-11 |           休日           |          振替休日          |        体育の日 振替休日         |
| 1994-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 1995-01-02 |           休日           |          振替休日          |          元日 振替休日           |
| 1995-01-16 |           休日           |          振替休日          |        成人の日 振替休日         |
| 1995-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 1996-02-12 |           休日           |          振替休日          |      建国記念の日 振替休日       |
| 1996-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 1996-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |
| 1996-09-16 |           休日           |          振替休日          |        敬老の日 振替休日         |
| 1996-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |
| 1997-07-21 |           休日           |          振替休日          |         海の日 振替休日          |
| 1997-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |
| 1998-05-04 |           休日           |          振替休日          |       憲法記念日 振替休日        |
| 1999-03-22 |           休日           |          振替休日          |        春分の日 振替休日         |
| 1999-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 1999-10-11 |           休日           |          振替休日          |        体育の日 振替休日         |
| 2000-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 2001-02-12 |           休日           |          振替休日          |      建国記念の日 振替休日       |
| 2001-04-30 |           休日           |          振替休日          |       みどりの日 振替休日        |
| 2001-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 2001-09-24 |           休日           |          振替休日          |        秋分の日 振替休日         |
| 2001-12-24 |           休日           |          振替休日          |       天皇誕生日 振替休日        |
| 2002-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 2002-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |
| 2002-09-16 |           休日           |          振替休日          |        敬老の日 振替休日         |
| 2002-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |
| 2003-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |
| 2004-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 2005-03-21 |           休日           |          振替休日          |        春分の日 振替休日         |
| 2005-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 2006-01-02 |           休日           |          振替休日          |          元日 振替休日           |
| 2006-05-04 |           休日           |         国民の休日         |            国民の休日            |
| 2007-02-12 |           休日           |          振替休日          |      建国記念の日 振替休日       |
| 2007-04-30 |           休日           |          振替休日          |        昭和の日 振替休日         |
| 2007-09-24 |           休日           |          振替休日          |        秋分の日 振替休日         |
| 2007-12-24 |           休日           |          振替休日          |       天皇誕生日 振替休日        |
| 2008-05-06 |           休日           |          振替休日          |       みどりの日 振替休日        |
| 2008-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |
| 2009-05-06 |           休日           |          振替休日          |       憲法記念日 振替休日        |
| 2009-09-22 |           休日           |         国民の休日         |            国民の休日            |
| 2010-03-22 |           休日           |          振替休日          |        春分の日 振替休日         |
| 2012-01-02 |           休日           |          振替休日          |          元日 振替休日           |
| 2012-04-30 |           休日           |          振替休日          |        昭和の日 振替休日         |
| 2012-12-24 |           休日           |          振替休日          |       天皇誕生日 振替休日        |
| 2013-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |
| 2013-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |
| 2014-05-06 |           休日           |          振替休日          |       みどりの日 振替休日        |
| 2014-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |
| 2015-05-06 |           休日           |          振替休日          |       憲法記念日 振替休日        |
| 2015-09-22 |           休日           |         国民の休日         |            国民の休日            |
| 2016-03-21 |           休日           |          振替休日          |        春分の日 振替休日         |
| 2017-01-02 |           休日           |          振替休日          |          元日 振替休日           |
| 2018-02-12 |           休日           |          振替休日          |      建国記念の日 振替休日       |
| 2018-04-30 |           休日           |          振替休日          |        昭和の日 振替休日         |
| 2018-09-24 |           休日           |          振替休日          |        秋分の日 振替休日         |
| 2018-12-24 |           休日           |          振替休日          |       天皇誕生日 振替休日        |
| 2019-04-30 |           休日           |         国民の休日         |            国民の休日            |
| 2019-05-01 |     休日（祝日扱い）     |       天皇の即位の日       |          天皇の即位の日          |
| 2019-05-02 |           休日           |         国民の休日         |            国民の休日            |
| 2019-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |
| 2019-08-12 |           休日           |          振替休日          |         山の日 振替休日          |
| 2019-10-14 | 体育の日（スポーツの日） |          体育の日          |             体育の日             |
| 2019-10-22 |     休日（祝日扱い）     | 即位礼正殿の儀が行われる日 |          即位礼正殿の儀          |
| 2019-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |
| 2020-02-24 |           休日           |          振替休日          |       天皇誕生日 振替休日        |
| 2020-05-06 |           休日           |          振替休日          |       憲法記念日 振替休日        |
| 2021-08-09 |           休日           |          振替休日          |         山の日 振替休日          |
| 2023-01-02 |           休日           |          振替休日          |          元日 振替休日           |
+------------+--------------------------+----------------------------+----------------------------------+
```
