'''
Crawler DAG definition.
'''

import datetime as dt
from os import path
from string import Template

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import BranchPythonOperator

PROJECT_PATH = path.abspath(path.join(path.dirname(__file__), '../..'))

DEFAULT_ARGS = {
    'owner': 'airflow',
    'start_date': dt.today().replace(day=1),
    'concurrency': 1,
    'retries': 0
}

def branch_tasks(execution_date, **kwargs):  # pylint: disable=unused-argument
    '''
    Branch the tasks based on weekday.
    '''
    # check if the execution day is 'Friday'
    if execution_date.weekday() == 3:
        return ['crawl_ddo_codes', 'crawl_expenditure', 'crawl_receipts']

    return ['crawl_expenditure', 'crawl_receipts']


with DAG('crawl_treasuries',
         default_args=DEFAULT_ARGS,
         schedule_interval='30 4 * * *',
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

    EXP_CRAWL_TASK = BashOperator(
        task_id='crawl_expenditure',
        bash_command=EXP_CRAWL_COMMAND.substitute(project_path=PROJECT_PATH),
        trigger_rule='none_failed'
    )

    REC_CRAWL_COMMAND = Template("""
        cd $project_path/scraper && scrapy crawl treasury_receipts -a start={{ ds_nodash }} -a end={{ ds_nodash }}
    """)

    REC_CRAWL_TASK = BashOperator(
        task_id='crawl_receipts',
        bash_command=REC_CRAWL_COMMAND.substitute(project_path=PROJECT_PATH),
        trigger_rule='none_failed'
    )

BRANCH_OP = BranchPythonOperator(
    task_id='branch_task',
    provide_context=True,
    python_callable=branch_tasks,
    dag=dag
)

CREATE_DIR.set_downstream(BRANCH_OP)
BRANCH_OP.set_downstream([CRAWL_DDO_CODES, EXP_CRAWL_TASK, REC_CRAWL_TASK])
CRAWL_DDO_CODES.set_downstream(EXP_CRAWL_TASK)
CRAWL_DDO_CODES.set_downstream(REC_CRAWL_TASK)
