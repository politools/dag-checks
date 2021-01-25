import os
from glob import glob

import airflow
from airflow import DAG
from airflow.models import DagBag
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.python_operator import PythonOperator
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.settings import DAGS_FOLDER
from airflow.utils.dates import days_ago
from sqlalchemy import event


class BaseCheck(object):  # pylint: disable=useless-object-inheritance
    def __init__(self, dag_folder=None):
        self.dag_folder = dag_folder or DAGS_FOLDER
        self.dag_bag = DagBag(include_examples=False, dag_folder=self.dag_folder)

    def get_errors(self):
        raise NotImplementedError()

    def check(self):
        msg_lines = ["\n"]
        msg_lines += ["CHECKING: {}".format(self.__class__.__name__)]
        try:
            errors = self.get_errors()
            if errors:
                msg_lines += ["CHECK FAILED!"]
                msg_lines.extend(errors)
            else:
                msg_lines += ["Everything is ok!"]
        except Exception as err:  # pylint: disable=broad-except
            msg_lines += ["There was an exception when checking {}".format(self.__class__.__name__)]
            msg_lines += [str(err)]
        print("\n".join(msg_lines))


class CheckEveryFileHasAtLeastOneDag(BaseCheck):
    def resolve_path(self, path):
        return os.path.relpath(path=path, start=self.dag_folder)

    def get_errors(self):
        errors = []
        dag_files = {self.resolve_path(d.filepath) for d in self.dag_bag.dags.values()}
        expected_dag_files = {
            self.resolve_path(f) for f in os.listdir(self.dag_folder) if not f.startswith("_")
        }
        for file in expected_dag_files - dag_files:
            errors.append(
                "File {} seems to have no DAGs. If that's intended "
                "consider adding it to .airflowignore".format(os.path.basename(file))
            )

        return errors


class CheckDAGShouldNotDoDbQueries(BaseCheck):
    class CountQueriesResult:
        def __init__(self):
            self.count = 0

    class CountQueries:
        """
        Counts the number of queries sent to Airflow Database in a given context.

        Does not support multiple processes. When a new process is started in context, its queries will
        not be included.
        """

        def __init__(self):
            self.result = CheckDAGShouldNotDoDbQueries.CountQueriesResult()

        def __enter__(self):
            event.listen(
                airflow.settings.engine,
                "after_cursor_execute",
                self.after_cursor_execute,
            )
            return self.result

        def __exit__(self, type_, value, traceback):
            event.remove(
                airflow.settings.engine,
                "after_cursor_execute",
                self.after_cursor_execute,
            )

        def after_cursor_execute(self, *args, **kwargs):  # pylint: disable=unused-argument
            self.result.count += 1

    def get_errors(self):
        dags = glob(self.dag_folder + "/*.py", recursive=True)
        errors = []
        for filepath in dags:
            with self.CountQueries() as result:
                DagBag(
                    dag_folder=filepath,
                    include_examples=False,
                )
                if result.count != 0:
                    errors.append("File {} has {} top level queries.".format(filepath, result.count))
        return errors


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


def check_function(*args, **kwargs):
    print("******* RUNNING DAGS CHECKS *******")
    CheckEveryFileHasAtLeastOneDag().check()
    CheckDAGShouldNotDoDbQueries().check()
    CheckOperatorsReferenceExistingDagTaskIds().check()


with DAG(dag_id="diagnose_dag", schedule_interval=None, start_date=days_ago(1)) as dag:
    PythonOperator(task_id="check_task", python_callable=check_function)
