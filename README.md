# Himachal Pradesh Fiscal Data explorer
Himachal Pradesh Fiscal Data explorer for [Open Budgets India](https://openbudgetsindia.org/) Platform.

### Setup Instructions for the Scraper

#### To setup the env, type the following commands in that order:

- `git clone https://github.com/CivicDataLab/hp-fiscal-data-explorer.git`
- `pip install pipenv`
- `cd scraper`
- `pipenv install --three --ignore-pipfile`

#### To Activate the environment once setup.

- `. $(pipenv --venv)/bin/activate`

#### Run the scraper for collecting ddo codes.
- `scrapy crawl ddo_collector`

#### Run the scraper for collecting datasets.
For Treasury Expenditure.
- `scrapy crawl treasury_expenditures -a start=20190501 -a end=20190531`

For Treasury Receipts.
- `scrapy crawl treasury_receipts -a start=20190501 -a end=20190531`
