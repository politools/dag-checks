import os

import pytest

from tests import TEST_FOLDER

os.environ["AIRFLOW_HOME"] = TEST_FOLDER
os.environ["AIRFLOW__CORE__SQL_ALCHEMY_CONN"] = "sqlite:///{}/airflow.db".format(TEST_FOLDER)


# pylint: disable=import-outside-toplevel


@pytest.fixture(scope="session", autouse=True)
def reset_db_fixture():
    from airflow.utils.db import resetdb

    try:
        # Airflow 1.10
        resetdb(None)  # pylint: disable=too-many-function-args
    except TypeError:
        # Airflow 2.0
        resetdb()  # pylint: disable=no-value-for-parameter
    yield
