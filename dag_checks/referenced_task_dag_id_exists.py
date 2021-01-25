from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor

from dag_checks.base import BaseCheck


class CheckOperatorsReferenceExistingDagTaskIds(BaseCheck):
    def __init__(self, *args, **kwargs):
        super(  # pylint: disable=super-with-arguments
            CheckOperatorsReferenceExistingDagTaskIds, self
        ).__init__(*args, **kwargs)
        self.dag_task_map = {d.dag_id: [t.task_id for t in d.tasks] for d in self.dag_bag.dags.values()}

    def get_errors(self):
        errors = []
        for dag in self.dag_bag.dags.values():
            for task in dag.tasks:
                if isinstance(task, ExternalTaskSensor):
                    # Make sure that the dag_id exists in other DAGs
                    external_dag_id = task.external_dag_id
                    external_task_id = task.external_task_id

                    if external_dag_id not in self.dag_task_map:
                        err = (
                            f"ExternalTaskSensor (task: {task.task_id}) in DAG {dag.dag_id} references "
                            f"dag_id that does not exist: {external_dag_id}"
                        )
                        errors.append(err)
                    if external_task_id is not None:
                        if external_task_id not in self.dag_task_map.get(external_dag_id, []):
                            err = (
                                f"ExternalTaskSensor (task: {task.task_id}) in DAG {dag.dag_id} references "
                                f"task_id {external_task_id} that does not exist in {external_dag_id}"
                            )
                            errors.append(err)
                elif isinstance(task, TriggerDagRunOperator):
                    # Make sure that TriggerDagRunOperator use existing dag_id
                    external_dag_id = task.trigger_dag_id
                    if external_dag_id not in self.dag_task_map:
                        err = (
                            f"TriggerDagRunOperator (task: {task.task_id}) in DAG {dag.dag_id} references "
                            f"dag_id that does not exist: {external_dag_id}"
                        )
                        errors.append(err)
        return errors
