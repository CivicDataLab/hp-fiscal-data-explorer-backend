'''
Crawler DAG definition.
'''

import datetime as dt
from os import path

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
# from airflow.operators.dagrun_operator import TriggerDagRunOperator

PROJECT_PATH = path.abspath(path.join(path.dirname(__file__), '../..'))

PRE_CRAWL_DT = dt.datetime(2019, 8, 23, 8, 45, 00)

with DAG('pre_treasury_crawl',
         default_args={
             'owner': 'airflow',
             'start_date': PRE_CRAWL_DT,
             'concurrency': 1,
             'retries': 0
         },
         schedule_interval='@once',
         catchup=False
        ) as dag:

    CREATE_DIR = BashOperator(
        task_id='create_datasets_dir',
        bash_command='cd {}/scraper && if [ ! -d datasets ]; then mkdir datasets; fi'.format(
            PROJECT_PATH
        )
    )

    CRAWL_DDO_CODES = BashOperator(
        task_id='crawl_ddo_codes',
        bash_command='cd {}/scraper && scrapy crawl ddo_collector'.format(PROJECT_PATH)
    )

# TRIGGER = TriggerDagRunOperator(
#     task_id='trigger_treasury_crawl',
#     trigger_dag_id="crawl_treasuries",
#     dag=dag,
# )

with DAG('crawl_treasuries',
         default_args={
             'owner': 'airflow',
             'start_date': PRE_CRAWL_DT + dt.timedelta(minutes=5),
             'concurrency': 1,
             'retries': 0
         },
         schedule_interval='*/5 * * * *',
         catchup=False
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
