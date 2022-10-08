# Backend for Himachal Pradesh Fiscal Data explorer

[![License: AGPLv3.0](https://img.shields.io/badge/License-MIT-lightgrey.svg)](https://github.com/CivicDataLab/hp-fiscal-data-explorer/blob/master/LICENSE)

## About

Himachal Pradesh Fiscal Data explorer for
[Open Budgets India](https://openbudgetsindia.org/) Platform.

### Setup Instructions for the Scraper

#### To setup the env, type the following commands in that order:

1. Fork the repository (Click the Fork button in the top right of this page,
   click your Profile Image)

2. Clone the forked repository to your local machine.

```markdown
git clone https://github.com/CivicDataLab/hp-fiscal-data-explorer.git
```

3. Install pipenv

```markdown
pip install pipenv
```

4. Change the present working directory

```markdown
cd scraper
```

```markdown
cp scraper/settings/settings.py scraper/settings/local.py
```

```markdown
pipenv install --three --ignore-pipfile
```

```markdown
cp scraper/settings/settings.py scraper/settings/local.py
```

- Edit the `scraper/settings/local.py` with setting values you want to keep like
  `DOWNLOAD_DELAY`, `CONCURRENT_REQUESTS` and custom settings like
  `DATASETS_PATH` etc.
- create a `datasets` directory at the path specified by `DATASET_PATH`
  variable. e.g. `hp-fiscal-data-explorer/scraper/datasets` if you didn't update
  the default value of the variable `DATASET_PATH`.

#### To Activate the environment once setup.

```markdown
. $(pipenv --venv)/bin/activate
```

#### Run the scraper for collecting ddo codes.

```markdown
scrapy crawl ddo_collector
```

#### Run the scraper for collecting datasets.

##### For Treasury Expenditure.

```markdown
scrapy crawl treasury_expenditures -a start=20190501 -a end=20190531
```

##### For Treasury Receipts.

```markdown
scrapy crawl treasury_receipts -a start=20190501 -a end=20190531
```

##### For Budget Expenditure.

```markdown
scrapy crawl budget_expenditures -a date=20190531
```

## NOTES:

- the arguments `start` and `end` specifies the date range for datasets. The
  date format is `yyyymmdd`.
- the datasets will be `CSV` files with name in the format:
  `treasury_expenditures_<treasury>_<ddo>_<timestamp>.csv` for expenditures.

## REPO STATUS

![GitHub PR Open](https://img.shields.io/github/issues-pr/CivicDataLab/hp-fiscal-data-explorer-backend?style=for-the-badge&color=aqua)
![GitHub PR closed](https://img.shields.io/github/issues-pr-closed-raw/CivicDataLab/hp-fiscal-data-explorer-backend?style=for-the-badge&color=blue)
![GitHub language count](https://img.shields.io/github/languages/count/CivicDataLab/hp-fiscal-data-explorer-backend?style=for-the-badge&color=brightgreen)
<br><br>

## Our Contributors

<a href="https://github.com/CivicDataLab/hp-fiscal-data-explorer-backend/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=CivicDataLab/hp-fiscal-data-explorer-backend" />
</a>

<br>
<div align="center">
Show some ❤️ by starring this awesome repository!
</div>
