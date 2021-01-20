import sys
from collections import namedtuple
from pathlib import Path

import black
from autoflake import fix_file
from isort import SortImports

AutoflakeArgs = namedtuple(
    "AutoflakeArgs",
    "remove_all_unused_imports "
    "ignore_init_module_imports "
    "remove_duplicate_keys "
    "remove_unused_variables "
    "in_place imports "
    "expand_star_imports "
    "check",
)


def remove_unused_imports(output_file_name: str) -> None:
    fix_file(
        output_file_name,
        args=AutoflakeArgs(
            remove_all_unused_imports=True,
            ignore_init_module_imports=False,
            imports=None,
            expand_star_imports=False,
            remove_duplicate_keys=False,
            remove_unused_variables=True,
            in_place=True,
            check=False,
        ),
        standard_out=sys.stdout,
    )


def format_with_black(output_file_name: str) -> None:
    black.format_file_in_place(
        Path(output_file_name),
        mode=black.FileMode(line_length=110),
        fast=False,
        write_back=black.WriteBack.YES,
    )


def sort_imports(output_file_name: str) -> None:
    SortImports(output_file_name)


def apply_cosmetics(output_file_name: str) -> None:
    remove_unused_imports(output_file_name)
    sort_imports(output_file_name)
    format_with_black(output_file_name)
