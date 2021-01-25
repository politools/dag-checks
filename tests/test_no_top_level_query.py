from dag_checks.no_top_level_query import CheckDAGShouldNotDoDbQueries
from tests import TEST_DAGS_FOLDER


class TestCheckEveryFileHasAtLeastOneDag:
    def test_check(self):  # pylint: disable=no-self-use
        check = CheckDAGShouldNotDoDbQueries(dag_folder=TEST_DAGS_FOLDER)
        errors = check.get_errors()
        assert len(errors) == 1
        assert "tests/dags/dag_no_top_level_query.py has 1 top level queries." in errors[0]
