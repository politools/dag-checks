from unittest import mock

from dag_checks.base import BaseCheck
from tests import TEST_DAGS_FOLDER


class TestBaseCheck:
    def test_check_init(self):  # pylint: disable=no-self-use
        check = BaseCheck(dag_folder=TEST_DAGS_FOLDER)
        assert check.dag_bag.dag_folder == check.dag_folder

    @mock.patch("dag_checks.base.BaseCheck.get_errors")
    def test_check_ok(self, mock_check, capsys):  # pylint: disable=no-self-use
        mock_check.return_value = []
        BaseCheck(dag_folder=TEST_DAGS_FOLDER).check()
        expected = """

CHECKING: BaseCheck
Everything is ok!
"""
        assert expected in capsys.readouterr().out

    @mock.patch("dag_checks.base.BaseCheck.get_errors")
    def test_check(self, mock_check, capsys):  # pylint: disable=no-self-use
        mock_check.return_value = ["An error when checking"]
        BaseCheck(dag_folder=TEST_DAGS_FOLDER).check()
        expected = """

CHECKING: BaseCheck
CHECK FAILED!
An error when checking
"""
        assert expected in capsys.readouterr().out
