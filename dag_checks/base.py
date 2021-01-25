from airflow.models import DagBag
from airflow.settings import DAGS_FOLDER


class BaseCheck(object):  # pylint: disable=useless-object-inheritance
    def __init__(self, dag_folder=None):
        self.dag_folder = dag_folder or DAGS_FOLDER
        self.dag_bag = DagBag(include_examples=False, dag_folder=self.dag_folder)

    def get_errors(self):
        raise NotImplementedError()

    def check(self):
        msg_lines = ["\n"]
        msg_lines += ["CHECKING: {}".format(self.__class__.__name__)]
        try:
            errors = self.get_errors()
            if errors:
                msg_lines += ["CHECK FAILED!"]
                msg_lines.extend(errors)
            else:
                msg_lines += ["Everything is ok!"]
        except Exception as err:  # pylint: disable=broad-except
            msg_lines += ["There was an exception when checking {}".format(self.__class__.__name__)]
            msg_lines += [str(err)]
        print("\n".join(msg_lines))
