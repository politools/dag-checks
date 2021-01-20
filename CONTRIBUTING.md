# Contributing
We welcome all contributions!

## Local development
To start develop locally follow the steps:
1. Clone the repository
1. Install the package in editable mode using `pip install -e ".[devel]"` (using
virtualenv is recommended)
1. Start developing! 🚀

Remember that the code of `dag_checks` and of `diagnosis_dag.py` has to be
compatible with:
- Apache Airflow 1.10.X
- Apache Airflow 2.X

and should support:
- Python 2.7
- Python 3.5+

## Pre-commits

This project is using [pre-commits](https://pre-commit.com) to ensure the quality of the code.
We encourage you to use pre-commits, but it's not required in order to contribute. Every change is checked
on CI and if it does not pass the tests it cannot be accepted. If you want to check locally then
you should install Python3.6 or newer together and run:
```bash
pip install pre-commit
# or
brew install pre-commit
```
For more installation options visit the [pre-commits](https://pre-commit.com).

To turn on pre-commit checks for commit operations in git, run:
```bash
pre-commit install
```
To run all checks on your staged files, run:
```bash
pre-commit run
```
To run all checks on all files, run:
```bash
pre-commit run --all-files
```
