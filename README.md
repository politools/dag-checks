# DAG checks

![CI](https://github.com/Polidea/dag-checks/workflows/CI/badge.svg?branch=main)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](https://opensource.org/licenses/Apache-2.0)

The `dag-checks` consist of checks that can help you in maintaining
your [Apache Airflow](https://airflow.apache.org) instance.

## Usage

There are two ways to use the tools from this repository:
- using the `dag_checks` package in your CI/CD system
- using `diagnosis_dag.py` in your Airflow deployment

### Using airflow-checks on CI/CD
1. Install the package using `pip install dag-checks`
2. Then in your tests you can simply use the checks like this:
```python
from dag_checks.no_top_level_query import CheckDAGShouldNotDoDbQueries

def test_dag_has_no_top_level_query():
    CheckDAGShouldNotDoDbQueries().check()
```

### Using the diagnose DAG

If you want quickly to discover some possible problems in your DAGs and
you don't want to bother with setting a CI/CD system (although we recommend
doing it) you can simply:
1. Copy and paste the `diagnosis_dag.py` file to your Airflow DAGs folder
2. Trigger this DAG from CLI or web ui
3. Analyze the log of the `diagnose_task` in this DAG. It should look similar to
this one:
```
[2021-01-20 18:22:32,240] {logging_mixin.py:104} INFO - ******* RUNNING DAGS CHECKS *******
[2021-01-20 18:22:33,327] {logging_mixin.py:104} INFO -

CHECKING: CheckEveryFileHasAtLeastOneDag
CHECK FAILED!
File tg.py seems to have no DAGs
File check_dag_ci.py seems to have no DAGs
[2021-01-20 18:22:33,329] {logging_mixin.py:104} INFO -
[2021-01-20 18:22:33,331] {dagbag.py:440} INFO - Filling up the DagBag from /files/dags
[2021-01-20 18:22:33,585] {dagbag.py:440} INFO - Filling up the DagBag from /files/dags/blogpost.py
[2021-01-20 18:22:33,722] {dagbag.py:440} INFO - Filling up the DagBag from /files/dags/branching.py
[2021-01-20 18:22:33,737] {dagbag.py:440} INFO - Filling up the DagBag from /files/dags/check_dag_ci.py
[2021-01-20 18:22:33,743] {dagbag.py:276} INFO - File /files/dags/check_dag_ci.py assumed to contain no DAGs. Skipping.
[2021-01-20 18:22:33,747] {dagbag.py:440} INFO - Filling up the DagBag from /files/dags/diagnosis_dag.py
[2021-01-20 18:22:33,760] {dagbag.py:440} INFO - Filling up the DagBag from /files/dags/none-from-time-to-time.py
[2021-01-20 18:22:33,774] {dagbag.py:440} INFO - Filling up the DagBag from /files/dags/td_test.py
[2021-01-20 18:22:33,789] {dagbag.py:440} INFO - Filling up the DagBag from /files/dags/templated_dag.py
[2021-01-20 18:22:33,831] {dagbag.py:440} INFO - Filling up the DagBag from /files/dags/tg.py
[2021-01-20 18:22:33,841] {dagbag.py:276} INFO - File /files/dags/tg.py assumed to contain no DAGs. Skipping.
[2021-01-20 18:22:33,844] {dagbag.py:440} INFO - Filling up the DagBag from /files/dags/the_old_issue.py
[2021-01-20 18:22:33,855] {dagbag.py:440} INFO - Filling up the DagBag from /files/dags/xcom.py
[2021-01-20 18:22:33,867] {logging_mixin.py:104} INFO -

CHECKING: CheckDAGShouldNotDoDbQueries
CHECK FAILED!
File /files/dags/templated_dag.py has 1 top level queries.
[2021-01-20 18:22:33,868] {logging_mixin.py:104} INFO -
[2021-01-20 18:22:33,869] {dagbag.py:440} INFO - Filling up the DagBag from /files/dags
[2021-01-20 18:22:34,072] {logging_mixin.py:104} INFO -

CHECKING: CheckOperatorsReferenceExistingDagTaskIds
CHECK FAILED!
TriggerDagRunOperator (task: trigger_2) in DAG test_dr references dag_id that does not exist: unknown```
```

## Contributing

We welcome all contributions! To learn more check the [CONTRIBUTING.md](/CONTRIBUTING.md).
