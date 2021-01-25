from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

with DAG(dag_id="dag_dagfile_has_dag_fail", schedule_interval=None, start_date=days_ago(1)):
    DummyOperator(task_id="test")
