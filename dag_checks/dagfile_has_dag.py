import os

from dag_checks.base import BaseCheck


class CheckEveryFileHasAtLeastOneDag(BaseCheck):
    def _check(self):
        errors = []
        dag_files = {d.filepath for d in self.dag_bag.dags.values()}
        # TODO: handle .airflowignore
        expected_dag_files = {
            os.path.join(self.dag_folder, f) for f in os.listdir(self.dag_folder) if not f.startswith("_")
        }
        for file in expected_dag_files - dag_files:
            errors.append("File {} seems to have no DAGs".format(file))

        return errors
