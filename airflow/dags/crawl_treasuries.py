'''
Crawler DAG definition.
'''

import datetime as dt
from os import path

from airflow import DAG
from airflow.operators.bash_operator import BashOperator

PROJECT_PATH = path.abspath(path.join(path.dirname(__file__), '../..'))

DEFAULT_ARGS = {
    'owner': 'airflow',
    'start_date': dt.datetime(2019, 8, 21, 13, 30, 00),
    'concurrency': 1,
    'retries': 0
}

with DAG('crawl_treasuries',
         default_args=DEFAULT_ARGS,
         schedule_interval='@daily',
        ) as dag:

    CRAWL_EXPENDITURE = BashOperator(
        task_id='crawl_expenditure',
        bash_command='''
            cd {}/scraper && scrapy crawl treasury_expenditures -a start=20190801 -a end=20190831
        '''.format(PROJECT_PATH)
    )

    CRAWL_RECEIPTS = BashOperator(
        task_id='crawl_receipts',
        bash_command='''
            cd {}/scraper && scrapy crawl treasury_receipts -a start=20190801 -a end=20190831
        '''.format(PROJECT_PATH)
    )

