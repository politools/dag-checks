from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.utils.dates import days_ago

with DAG(
    dag_id="dag_referenced_task_dag_id_exists_fail", schedule_interval=None, start_date=days_ago(1)
) as dag:
    TriggerDagRunOperator(task_id="test_trigger", trigger_dag_id="nonexistent")
    ExternalTaskSensor(task_id="test_sensor_dag", external_dag_id="nonexistent")
    ExternalTaskSensor(task_id="test_sensor_task", external_dag_id="nonexistent", external_task_id="non-task")
