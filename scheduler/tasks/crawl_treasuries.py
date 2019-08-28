'''
Crawler DAG definition.
'''

import datetime as dt
from os import path
from string import Template

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

    EXP_CRAWL_COMMAND = Template("""
        cd $project_path/scraper && scrapy crawl treasury_expenditures -a start={{ ds_nodash }} -a end={{ ds_nodash }}
    """)

    CRAWL_EXPENDITURE = BashOperator(
        task_id='crawl_expenditure',
        bash_command=EXP_CRAWL_COMMAND.substitute(project_path=PROJECT_PATH)
    )

    REC_CRAWL_COMMAND = Template("""
        cd $project_path/scraper && scrapy crawl treasury_receipts -a start={{ ds_nodash }} -a end={{ ds_nodash }}
    """)

    CRAWL_RECEIPTS = BashOperator(
        task_id='crawl_receipts',
        bash_command=REC_CRAWL_COMMAND.substitute(project_path=PROJECT_PATH)
    )
