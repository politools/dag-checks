from dag_checks.referenced_task_dag_id_exists import (
    CheckOperatorsReferenceExistingDagTaskIds,
)
from tests import TEST_DAGS_FOLDER


class TestCheckOperatorsReferenceExistingDagTaskIds:
    def test_check(self):  # pylint: disable=no-self-use
        check = CheckOperatorsReferenceExistingDagTaskIds(dag_folder=TEST_DAGS_FOLDER)
        errors = check.get_errors()
        expected_errors = [
            "TriggerDagRunOperator (task: test_trigger) in DAG dag_referenced_task_dag_id_exists_fail "
            "references dag_id that does not exist: nonexistent",
            "ExternalTaskSensor (task: test_sensor_dag) in DAG dag_referenced_task_dag_id_exists_fail "
            "references dag_id that does not exist: nonexistent",
            "ExternalTaskSensor (task: test_sensor_task) in DAG dag_referenced_task_dag_id_exists_fail "
            "references dag_id that does not exist: nonexistent",
            "ExternalTaskSensor (task: test_sensor_task) in DAG dag_referenced_task_dag_id_exists_fail "
            "references task_id non-task that does not exist in nonexistent",
        ]
        assert len(errors) == 4
        assert set(errors) == set(expected_errors)
