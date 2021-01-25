import ast
import importlib
import inspect
import os
import sys
from typing import List, NamedTuple, Optional, Tuple

from jinja2 import Template

from cosmetics import apply_cosmetics
from tests import TEST_FOLDER

# Set this before importing Airflow
os.environ["AIRFLOW_HOME"] = TEST_FOLDER
os.environ["AIRFLOW__CORE__SQL_ALCHEMY_CONN"] = "sqlite:///{}/airflow.db".format(TEST_FOLDER)

from dag_checks.base import BaseCheck  # pylint: disable=wrong-import-position

NL = "\n"
KNOW_NEEDED_CLASSES = {BaseCheck}

CHECK_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "dag_checks")
DAG_FILE_PATH = "diagnosis_dag.py"


class Import(NamedTuple):
    module: List[str] = []
    name: List[str] = []
    alias: Optional[str] = None

    def __str__(self):
        if self.name and self.module:
            module_name = ".".join(self.module)
            import_str = f"from {module_name} import {self.name[0]}"
            import_str = f"{import_str} as {self.alias}" if self.alias else import_str
        else:
            import_str = f"import {self.name[0]}"
        return import_str


def get_imports(file_path: str):
    with open(file_path) as file:
        root = ast.parse(file.read(), file_path)

    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Import):
            module = []
        elif isinstance(node, ast.ImportFrom):
            module = node.module.split(".")
        else:
            continue

        for name in node.names:
            yield Import(module, name.name.split("."), name.asname)


def get_check_class(mod_path: str) -> List[BaseCheck]:
    mod = importlib.import_module(mod_path)
    check_classes = set()
    for attr in mod.__dict__.keys():
        obj = getattr(mod, attr)
        if inspect.isclass(obj):
            if BaseCheck in obj.__bases__:
                check_classes.add(obj)
            if mod_path == "dag_checks.base" and obj in KNOW_NEEDED_CLASSES:
                check_classes.add(obj)
    return list(check_classes)


def parse_all_checks() -> Tuple[List[Import], List[BaseCheck]]:
    imports = []
    check_classes = []

    for file in sorted(os.listdir(CHECK_FOLDER)):
        file_path = os.path.join(CHECK_FOLDER, file)
        if not os.path.isfile(file_path):
            continue
        imports.extend(get_imports(file_path))
        check_classes.extend(get_check_class(f"dag_checks.{file.replace('.py', '')}"))

    return imports, sorted(check_classes, key=lambda x: x.__class__.__name__)


def prepare_check_code(imports, check_classes) -> str:
    lines = NL.join(str(imp) for imp in imports)
    lines += NL
    lines += NL.join(inspect.getsource(cls) + NL for cls in check_classes)
    return lines


CHECK_CALLABLE_TEMPLATE = """
def check_function(*args, **kwargs):
    print("******* RUNNING DAGS CHECKS *******")
    {% for cls in check_classes %}{{ cls.__name__ }}().check()
    {% endfor %}
"""


def prepare_callable_code(check_classes: List) -> str:
    return Template(CHECK_CALLABLE_TEMPLATE).render(check_classes=check_classes)


DAG_IMPORTS = [
    Import(module=["airflow"], name=["DAG"]),
    Import(module=["airflow", "utils", "dates"], name=["days_ago"]),
    Import(module=["airflow", "operators", "python_operator"], name=["PythonOperator"]),
]
DAG_TEMPLATE = """
with DAG(dag_id="diagnose_dag", schedule_interval=None, start_date=days_ago(1)) as dag:
    PythonOperator(
        task_id="check_task",
        python_callable=check_function
    )
"""


def prepare_dag_code():
    imports, check_classes = parse_all_checks()
    imports.extend(DAG_IMPORTS)
    imports = [i for i in imports if not str(i).startswith("from dag_checks.")]

    source_code = prepare_check_code(imports, check_classes)
    callable_code = prepare_callable_code([c for c in check_classes if BaseCheck in c.__bases__])
    with open(DAG_FILE_PATH, "w+") as file:
        file.write(source_code)
        file.write(callable_code)
        file.write(DAG_TEMPLATE)
        file.flush()
        apply_cosmetics(file.name)

    sys.exit(0)


if __name__ == "__main__":
    prepare_dag_code()
