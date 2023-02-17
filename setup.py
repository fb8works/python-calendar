# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = {"": "src"}

packages = ["python_calendar", "python_calendar.test", "python_calendar.test.holidays"]

package_data = {"": ["*"], "python_calendar": ["styles/*"]}

install_requires = [
    "click>=8.1.3,<9.0.0",
    "holidays>=0.18,<0.19",
    "python-dateutil>=2.7.0,<3.0.0",
]

entry_points = {"console_scripts": ["pycal = python_calendar.cli:main"]}

setup_kwargs = {
    "name": "python-calendar",
    "version": "0.1.0",
    "description": "Python Calendar",
    "long_description": "# python-calendar\n\n[![Python Lint & Test](https://github.com/fb8works/python-calendar/actions/workflows/python-app-custom.yml/badge.svg)](https://github.com/fb8works/python-calendar/actions/workflows/python-app-custom.yml)\n\nTool to create an anual calendar available in Excel.\n\nシンプルな４月始まりのカレンダーを html で生成します。\nコピーする事で excel に貼り付ける事ができます。\n\n![screenshot](https://github.com/fb8works/python-calendar/blob/main/screenshot.png?raw=true)\n\n## Requirements\n\n- Python 3.8.0 or later\n\n## Install\n\n```bash\npip install git+https://github.com/fb8works/python-calendar.git\n```\n\n## Generate calendar\n\nGenerate a calendar for this year.\n\n```bash\npycal\n```\n\n## Specify the year and start month\n\n```bash\npycal --year=2023 --start-month=1\n```\n\n## Change the number of columns\n\n```bash\npycal --width=4\n```\n\n## Locale\n\nYou can change the calendar locale. Defaults to LC_ALL, LC_TIME, LANG environment variable or 'C'.\n\n```bash\npycal --locale=en_US\n```\n\n## Country\n\nYou can change the region of country that determines the holiday. default is same as locale.\n\n```bash\npycal --country=JP\n```\n\n## Subdivision\n\nThe subdivisions can be specified. eg. for california.\n\n```bash\npycal --locale=en_US --subdiv=CA\n```\n\n## Financial holiday\n\nIf you want clendar that uses financial holidays. The --country option is ignored.\n\n```bash\npycal --financial=NYSE\n```\n\n## Style sheet\n\nカレンダーを生成するとカレントディレクトリに calendar.css が生成されます。\nスタイルシートを編集することで祝日の色等を変更する事ができます。\n\n```css\n.holiday {\n    background: red;\n}\n.day.sun {\n    background: pink;\n}\n.day.sat {\n    background: skyblue;\n}\n```\n\n## NOTE\n\n[内閣府の祝日データ](https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html) と holidays, jpholidays モジュールの相違を比較検証します。\n\n```bash\n$ make test-verify\n```\n\n```\n+------------+--------------------------+----------------------------+----------------------------------+\n|    Date    |        Syukujitsu        |          Holidays          |            JPHoliday             |\n+------------+--------------------------+----------------------------+----------------------------------+\n| 1955-05-04 |            -             |             -              |            国民の休日            |\n| 1956-05-04 |            -             |             -              |            国民の休日            |\n| 1957-05-04 |            -             |             -              |            国民の休日            |\n| 1959-04-10 |         結婚の儀         |          結婚の儀          |    皇太子・明仁親王の結婚の儀    |\n| 1959-05-04 |            -             |             -              |            国民の休日            |\n| 1960-05-04 |            -             |             -              |            国民の休日            |\n| 1961-05-04 |            -             |             -              |            国民の休日            |\n| 1962-05-04 |            -             |             -              |            国民の休日            |\n| 1963-05-04 |            -             |             -              |            国民の休日            |\n| 1964-05-04 |            -             |             -              |            国民の休日            |\n| 1965-05-04 |            -             |             -              |            国民の休日            |\n| 1966-05-04 |            -             |             -              |            国民の休日            |\n| 1967-05-04 |            -             |             -              |            国民の休日            |\n| 1968-05-04 |            -             |             -              |            国民の休日            |\n| 1970-05-04 |            -             |             -              |            国民の休日            |\n| 1971-05-04 |            -             |             -              |            国民の休日            |\n| 1972-05-04 |            -             |             -              |            国民の休日            |\n| 1973-02-12 |            -             |             -              |      建国記念の日 振替休日       |\n| 1973-04-30 |           休日           |          振替休日          |       天皇誕生日 振替休日        |\n| 1973-05-04 |            -             |             -              |            国民の休日            |\n| 1973-09-24 |           休日           |          振替休日          |        秋分の日 振替休日         |\n| 1974-05-04 |            -             |             -              |            国民の休日            |\n| 1974-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |\n| 1974-09-16 |           休日           |          振替休日          |        敬老の日 振替休日         |\n| 1974-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |\n| 1975-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |\n| 1976-05-04 |            -             |             -              |            国民の休日            |\n| 1976-10-11 |           休日           |          振替休日          |        体育の日 振替休日         |\n| 1977-05-04 |            -             |             -              |            国民の休日            |\n| 1978-01-02 |           休日           |          振替休日          |          元日 振替休日           |\n| 1978-01-16 |           休日           |          振替休日          |        成人の日 振替休日         |\n| 1978-05-04 |            -             |             -              |            国民の休日            |\n| 1979-02-12 |           休日           |          振替休日          |      建国記念の日 振替休日       |\n| 1979-04-30 |           休日           |          振替休日          |       天皇誕生日 振替休日        |\n| 1979-05-04 |            -             |             -              |            国民の休日            |\n| 1980-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |\n| 1981-05-04 |           休日           |          振替休日          |       憲法記念日 振替休日        |\n| 1982-03-22 |           休日           |          振替休日          |        春分の日 振替休日         |\n| 1982-05-04 |            -             |             -              |            国民の休日            |\n| 1982-10-11 |           休日           |          振替休日          |        体育の日 振替休日         |\n| 1983-05-04 |            -             |             -              |            国民の休日            |\n| 1984-01-02 |           休日           |          振替休日          |          元日 振替休日           |\n| 1984-01-16 |           休日           |          振替休日          |        成人の日 振替休日         |\n| 1984-04-30 |           休日           |          振替休日          |       天皇誕生日 振替休日        |\n| 1984-05-04 |            -             |             -              |            国民の休日            |\n| 1984-09-24 |           休日           |          振替休日          |        秋分の日 振替休日         |\n| 1985-05-04 |            -             |             -              |            国民の休日            |\n| 1985-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |\n| 1985-09-16 |           休日           |          振替休日          |        敬老の日 振替休日         |\n| 1985-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |\n| 1986-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |\n| 1987-05-04 |           休日           |          振替休日          |       憲法記念日 振替休日        |\n| 1988-03-21 |           休日           |          振替休日          |        春分の日 振替休日         |\n| 1988-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 1988-12-23 |            -             |             -              |            天皇誕生日            |\n| 1989-01-02 |           休日           |          振替休日          |          元日 振替休日           |\n| 1989-01-16 |           休日           |          振替休日          |        成人の日 振替休日         |\n| 1989-02-24 |         大喪の礼         |          大喪の礼          |        昭和天皇の大喪の礼        |\n| 1989-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 1990-02-12 |           休日           |          振替休日          |      建国記念の日 振替休日       |\n| 1990-04-30 |           休日           |          振替休日          |       みどりの日 振替休日        |\n| 1990-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 1990-09-24 |           休日           |          振替休日          |        秋分の日 振替休日         |\n| 1990-11-12 |      即位礼正殿の儀      |       即位礼正殿の儀       |         即位の礼正殿の儀         |\n| 1990-12-24 |           休日           |          振替休日          |       天皇誕生日 振替休日        |\n| 1991-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 1991-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |\n| 1991-09-16 |           休日           |          振替休日          |        敬老の日 振替休日         |\n| 1991-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |\n| 1992-05-04 |           休日           |          振替休日          |       憲法記念日 振替休日        |\n| 1993-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 1993-06-09 |         結婚の儀         |          結婚の儀          | 皇太子・皇太子徳仁親王の結婚の儀 |\n| 1993-10-11 |           休日           |          振替休日          |        体育の日 振替休日         |\n| 1994-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 1995-01-02 |           休日           |          振替休日          |          元日 振替休日           |\n| 1995-01-16 |           休日           |          振替休日          |        成人の日 振替休日         |\n| 1995-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 1996-02-12 |           休日           |          振替休日          |      建国記念の日 振替休日       |\n| 1996-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 1996-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |\n| 1996-09-16 |           休日           |          振替休日          |        敬老の日 振替休日         |\n| 1996-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |\n| 1997-07-21 |           休日           |          振替休日          |         海の日 振替休日          |\n| 1997-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |\n| 1998-05-04 |           休日           |          振替休日          |       憲法記念日 振替休日        |\n| 1999-03-22 |           休日           |          振替休日          |        春分の日 振替休日         |\n| 1999-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 1999-10-11 |           休日           |          振替休日          |        体育の日 振替休日         |\n| 2000-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 2001-02-12 |           休日           |          振替休日          |      建国記念の日 振替休日       |\n| 2001-04-30 |           休日           |          振替休日          |       みどりの日 振替休日        |\n| 2001-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 2001-09-24 |           休日           |          振替休日          |        秋分の日 振替休日         |\n| 2001-12-24 |           休日           |          振替休日          |       天皇誕生日 振替休日        |\n| 2002-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 2002-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |\n| 2002-09-16 |           休日           |          振替休日          |        敬老の日 振替休日         |\n| 2002-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |\n| 2003-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |\n| 2004-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 2005-03-21 |           休日           |          振替休日          |        春分の日 振替休日         |\n| 2005-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 2006-01-02 |           休日           |          振替休日          |          元日 振替休日           |\n| 2006-05-04 |           休日           |         国民の休日         |            国民の休日            |\n| 2007-02-12 |           休日           |          振替休日          |      建国記念の日 振替休日       |\n| 2007-04-30 |           休日           |          振替休日          |        昭和の日 振替休日         |\n| 2007-09-24 |           休日           |          振替休日          |        秋分の日 振替休日         |\n| 2007-12-24 |           休日           |          振替休日          |       天皇誕生日 振替休日        |\n| 2008-05-06 |           休日           |          振替休日          |       みどりの日 振替休日        |\n| 2008-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |\n| 2009-05-06 |           休日           |          振替休日          |       憲法記念日 振替休日        |\n| 2009-09-22 |           休日           |         国民の休日         |            国民の休日            |\n| 2010-03-22 |           休日           |          振替休日          |        春分の日 振替休日         |\n| 2012-01-02 |           休日           |          振替休日          |          元日 振替休日           |\n| 2012-04-30 |           休日           |          振替休日          |        昭和の日 振替休日         |\n| 2012-12-24 |           休日           |          振替休日          |       天皇誕生日 振替休日        |\n| 2013-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |\n| 2013-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |\n| 2014-05-06 |           休日           |          振替休日          |       みどりの日 振替休日        |\n| 2014-11-24 |           休日           |          振替休日          |      勤労感謝の日 振替休日       |\n| 2015-05-06 |           休日           |          振替休日          |       憲法記念日 振替休日        |\n| 2015-09-22 |           休日           |         国民の休日         |            国民の休日            |\n| 2016-03-21 |           休日           |          振替休日          |        春分の日 振替休日         |\n| 2017-01-02 |           休日           |          振替休日          |          元日 振替休日           |\n| 2018-02-12 |           休日           |          振替休日          |      建国記念の日 振替休日       |\n| 2018-04-30 |           休日           |          振替休日          |        昭和の日 振替休日         |\n| 2018-09-24 |           休日           |          振替休日          |        秋分の日 振替休日         |\n| 2018-12-24 |           休日           |          振替休日          |       天皇誕生日 振替休日        |\n| 2019-04-30 |           休日           |         国民の休日         |            国民の休日            |\n| 2019-05-01 |     休日（祝日扱い）     |       天皇の即位の日       |          天皇の即位の日          |\n| 2019-05-02 |           休日           |         国民の休日         |            国民の休日            |\n| 2019-05-06 |           休日           |          振替休日          |       こどもの日 振替休日        |\n| 2019-08-12 |           休日           |          振替休日          |         山の日 振替休日          |\n| 2019-10-14 | 体育の日（スポーツの日） |          体育の日          |             体育の日             |\n| 2019-10-22 |     休日（祝日扱い）     | 即位礼正殿の儀が行われる日 |          即位礼正殿の儀          |\n| 2019-11-04 |           休日           |          振替休日          |        文化の日 振替休日         |\n| 2020-02-24 |           休日           |          振替休日          |       天皇誕生日 振替休日        |\n| 2020-05-06 |           休日           |          振替休日          |       憲法記念日 振替休日        |\n| 2021-08-09 |           休日           |          振替休日          |         山の日 振替休日          |\n| 2023-01-02 |           休日           |          振替休日          |          元日 振替休日           |\n+------------+--------------------------+----------------------------+----------------------------------+\n```\n",
    "author": "Daisuke Arai",
    "author_email": "daisuke.qu@gmail.com",
    "maintainer": "None",
    "maintainer_email": "None",
    "url": "None",
    "package_dir": package_dir,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "entry_points": entry_points,
    "python_requires": ">=3.8.0,<4.0.0",
}


setup(**setup_kwargs)  # type: ignore
