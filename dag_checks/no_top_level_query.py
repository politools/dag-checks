from glob import glob

import airflow.settings
from airflow.models import DagBag
from sqlalchemy import event

from dag_checks.base import BaseCheck


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
