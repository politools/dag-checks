from airflow import DAG
from airflow.models import Variable
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from airflow.utils.db import create_session

with create_session() as session:
    session.query(Variable).all()


with DAG(dag_id="dag_no_top_level_query_fail", schedule_interval=None, start_date=days_ago(1)) as dag:
    DummyOperator(task_id="test")
