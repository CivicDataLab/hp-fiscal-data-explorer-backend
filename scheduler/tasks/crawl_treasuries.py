'''
Crawler DAG definition.
'''

import datetime as dt
from os import path
from string import Template

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import ShortCircuitOperator

PROJECT_PATH = path.abspath(path.join(path.dirname(__file__), '../..'))

DEFAULT_ARGS = {
    'owner': 'airflow',
    'start_date': dt.datetime(2019, 8, 21),
    'concurrency': 1,
    'retries': 0
}

def check_trigger_week(execution_date, **kwargs):
    '''
    check if the execution day is 'Tuesday'
    '''
    return execution_date.weekday() == 2


with DAG('crawl_treasuries',
         default_args=DEFAULT_ARGS,
         schedule_interval='00 10 * * *',
         # catchup=False
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

CHECK_TRIGGER_WEEKLY = ShortCircuitOperator(
    task_id='check_trigger_weekly',
    python_callable=check_trigger_week,
    provide_context=True,
    dag=dag
)

CREATE_DIR.set_downstream(CRAWL_DDO_CODES)
CHECK_TRIGGER_WEEKLY.set_downstream(CRAWL_DDO_CODES)
CRAWL_DDO_CODES.set_downstream(CRAWL_EXPENDITURE)
CRAWL_DDO_CODES.set_downstream(CRAWL_RECEIPTS)
