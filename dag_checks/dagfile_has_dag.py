import os

from dag_checks.base import BaseCheck


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
