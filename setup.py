import os

from setuptools import setup

version = "1.0.0dev"

DEVEL_REQUIREMENTS = [
    "autoflake==1.3",
    "black==20.8b1",
    "isort==4.3.21",
    "jinja2",
    "pre-commit==2.9.3",
    "pylint==2.6.0",
    "pytest",
]

EXTRAS_REQUIREMENTS = {"devel": DEVEL_REQUIREMENTS}


def get_long_description():
    description = ""
    try:
        with open(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "README.md"),
            encoding="utf-8",
        ) as file:
            description = file.read()
    except FileNotFoundError:
        pass
    return description


def do_setup():
    setup(
        version=version,
        extras_require=EXTRAS_REQUIREMENTS,
    )


if __name__ == "__main__":
    do_setup()
