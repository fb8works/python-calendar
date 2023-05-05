# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['python_calendar', 'python_calendar.test', 'python_calendar.test.holidays']

package_data = \
{'': ['*'], 'python_calendar': ['styles/*']}

install_requires = \
['click>=8.1.3,<9.0.0',
 'holidays>=0.18,<0.19',
 'inscriptis>=2.3.2,<3.0.0',
 'python-dateutil>=2.7.0,<3.0.0',
 'setuptools>=67.4.0,<68.0.0']

entry_points = \
{'console_scripts': ['pycal = python_calendar.cli:main']}

setup_kwargs = {
    'name': 'python-calendar',
    'version': '0.1.7',
    'description': 'Python Calendar',
    'long_description': "# python-calendar\n\n[![Python Lint & Test](https://github.com/fb8works/python-calendar/actions/workflows/python-app-custom.yml/badge.svg)](https://github.com/fb8works/python-calendar/actions/workflows/python-app-custom.yml)\n\nHoliday calendar utility with HTML output.\n\n祝日を含むカレンダーを表示／生成するツール。\nコピーする事で excel に貼り付ける事ができます。\n\n![screenshot](https://github.com/fb8works/python-calendar/blob/main/screenshot.png?raw=true)\n\n## Requirements\n\n- Python 3.8.0 or later\n- elinks (OPTIONAL)\n\n## Install\n\n```bash\npip install git+https://github.com/fb8works/python-calendar.git\n```\n\n## Show calendar with holidays\n\nPrint a calendar for this month. requires w3m or elinks. you must install elinks if you want color.\n\n```bash\npycal\n```\n\nAnual calendar for this year.\n\n```bash\npycal .\n```\n\n## HTML calendar\n\nShow the anual calendar in browser.\n\n```bash\npycal . -H\n```\n\nGenerate HTML calendar for this year.\n\n```bash\npycal -o calendar.html\n```\n\n## Arguments and options\n\n```\n$ pycal --help\nUsage: pycal [OPTIONS] [ARGS]...\n\nOptions:\n  -t, --text                      Text mode\n  -H, --html                      HTML mode\n  -w, --width INTEGER RANGE       Width of columns.  [1<=x<=12]\n  -m, --start-month INTEGER RANGE\n                                  Start month.  [1<=x<=12]\n  -d, --first-weekday [mon|tue|wed|thu|fri|sat|sun]\n                                  First weekday.  [default: sun]\n  -o, --output TEXT               Output HTML filename.\n  -h, --holidays                  Include holiday list.\n  -l, --list-holidays             List holidays.\n  -c, --css TEXT                  Output css filename. (relative from output\n                                  directory)\n  -e, --use-external-css          Use external css file.\n  --css-href TEXT                 CSS location or URL.\n  -s, --style [default|simple]    CSS template name.  [default: default]\n  --encoding TEXT                 Character encoding for HTML.\n  --locale TEXT                   Locale eg. en_US.UTF-8.\n  -C, --country TEXT              Country code for holidays. eg. US (default\n                                  is same as locale)\n  --subdiv TEXT                   Specify subdivision.\n  --financial TEXT                Use financial holiday.\n  -f, --force                     Force overwrite css file.\n  -q, --quiet                     Quiet mode.\n  -n, --no-browser                Do not open browser.\n  -c, --color                     color mode (text mode).\n  -v, --verbose                   Show information.\n  --help                          Show this message and exit.\n```\n\n## Locale\n\nYou can change the calendar locale. Defaults to LC_ALL, LC_TIME, LANG environment variable or 'C'.\n\n```bash\npycal --locale=en_US\n```\n\n## Country\n\nYou can change the region of country that determines the holiday. default is same as locale.\n\n```bash\npycal --country=JP\n```\n\n## Subdivision\n\nThe subdivisions can be specified. eg. for california.\n\n```bash\npycal --locale=en_US --subdiv=CA\n```\n\n## Financial holiday\n\nIf you want clendar that uses financial holidays. The --country option is ignored.\n\n```bash\npycal --financial=NYSE\n```\n\n## Style sheet\n\nHTML カレンダーを生成するとカレントディレクトリに calendar.css が生成されます。\nスタイルシートを編集することで祝日の色等を変更する事ができます。 --inline-css オプションを指定した場合は css は生成されません。\n\n```css\n.holiday {\n    background: red;\n}\n.day.sun {\n    background: pink;\n}\n.day.sat {\n    background: skyblue;\n}\n```\n\n## NOTE\n\n[内閣府の祝日データ](https://www8.cao.go.jp/chosei/shukujitsu/gaiyou.html) と holidays, jpholidays モジュールの相違を比較検証します。\n\n```bash\n$ make test-verify\n```\n",
    'author': 'Daisuke Arai',
    'author_email': 'daisuke.qu@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.0,<4.0.0',
}


setup(**setup_kwargs)  # type: ignore
