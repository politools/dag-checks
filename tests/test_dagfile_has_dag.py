from dag_checks.dagfile_has_dag import CheckEveryFileHasAtLeastOneDag
from tests import TEST_DAGS_FOLDER


class TestCheckEveryFileHasAtLeastOneDag:
    def test_check(self):  # pylint: disable=no-self-use
        check = CheckEveryFileHasAtLeastOneDag(dag_folder=TEST_DAGS_FOLDER)
        errors = check.get_errors()
        assert errors == [
            "File dag_dagfile_has_dag.py seems to have no DAGs. If that's "
            "intended consider adding it to .airflowignore"
        ]
