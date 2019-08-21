'''
pre_crawl_dag
'''

import datetime as dt
from os import path

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dagrun_operator import TriggerDagRunOperator

PROJECT_PATH = path.abspath(path.join(path.dirname(__file__), '../..'))

DEFAULT_ARGS = {
    'owner': 'airflow',
    'start_date': dt.datetime(2019, 8, 21, 13, 30, 00),
    'concurrency': 1,
    'retries': 0
}

with DAG('pre_treasury_crawl',
         default_args=DEFAULT_ARGS,
         schedule_interval='@once',
        ) as dag:

    CRAWL_DDO_CODES = BashOperator(
        task_id='crawl_ddo_codes',
        bash_command='cd {}/scraper && scrapy crawl ddo_collector'.format(PROJECT_PATH)
    )

TRIGGER = TriggerDagRunOperator(
    task_id='trigger_treasury_crawl',
    trigger_dag_id="crawl_treasuries",
    dag=dag,
)
