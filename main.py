#!/usr/bin/env python3
# www.jrodal.com

import importlib
import os
import shutil
import click
import aocd

from enum import Enum

from rich.markdown import Markdown
from rich.traceback import install
from aoc_utils.log_runtime import print_runtime_table

from aoc_utils.base_solver import ProblemPart
from aoc_utils.rich_test_runner import RichTestRunner
from aoc_utils.walk_directory import walk_directory

from consts import YEAR, DAY, CONSOLE


def gen_solution_dir(day: int, year: int) -> str:
    return os.path.join(f"py{year}", f"day{day}")


class Task(Enum):
    RUN_PART1_TESTS = "Running Part1 tests"
    SOLVE_PART1 = "Solving Part1"
    RUN_PART2_TESTS = "Running Part2 tests"
    SOLVE_PART2 = "Solving Part2"


@click.group()
def cli() -> None:
    pass


@cli.command()
@click.option("--year", default=YEAR, type=int, help="Year to solve")
@click.option("--day", default=DAY, type=int, help="Day to solve")
def init(
    day: int,
    year: int,
) -> None:
    p = gen_solution_dir(day, year)
    shutil.copytree("templates", p)
    walk_directory(p, CONSOLE)


@cli.command()
@click.option(
    "--log-locals",
    is_flag=True,
    show_default=True,
    default=False,
    help="Log local variables in traceback",
)
@click.option(
    "--skip-part2",
    is_flag=True,
    show_default=True,
    default=False,
    help="Don't run part2",
)
@click.option(
    "--skip-part1",
    is_flag=True,
    show_default=True,
    default=False,
    help="Don't run part1",
)
@click.option(
    "--skip-tests", is_flag=True, show_default=True, default=False, help="Year to solve"
)
@click.option("--year", default=YEAR, type=int, help="Year to solve")
@click.option("--day", default=DAY, type=int, help="Day to solve")
def solve(
    day: int,
    year: int,
    skip_tests: bool,
    skip_part1: bool,
    skip_part2: bool,
    log_locals: bool,
) -> None:
    day = day
    year = year

    install(suppress=[click], show_locals=log_locals)

    module_path = gen_solution_dir(day, year).replace("/", ".")
    tests_module = importlib.import_module(f"{module_path}.tests")
    solution_module = importlib.import_module(f"{module_path}.solution")
    solver_kls = solution_module.Solver

    runtime_objects = {}
    for part, tests in (
        (
            ProblemPart.PART1 if not skip_part1 else None,
            tests_module.PartOneUnitTests if not skip_tests else None,
        ),
        (
            ProblemPart.PART2 if not skip_part2 else None,
            tests_module.PartTwoUnitTests if not skip_tests else None,
        ),
    ):
        if not part:
            continue
        CONSOLE.print(Markdown(f"# {part.name}"))
        if solver_kls.is_not_implemented(part):
            CONSOLE.print(f"[red] {part.name} not implemented [/red]")
            continue
        if tests:
            CONSOLE.print(Markdown("## Tests"))
            RichTestRunner(
                tb_locals=log_locals,
            ).make_suite_and_run(tests)
        CONSOLE.print(Markdown("## Solve Puzzle Input"))
        _, runtime = solver_kls(
            data=aocd.get_data(day=day, year=year)
        ).solve_and_submit(part, day=day, year=year)
        runtime_objects[part] = runtime

    print_runtime_table(
        runtime_objects.get(ProblemPart.PART1),
        runtime_objects.get(ProblemPart.PART2),
        CONSOLE,
    )


if __name__ == "__main__":
    cli()
