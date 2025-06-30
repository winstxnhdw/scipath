from collections.abc import Iterator
from csv import reader
from pathlib import Path

from pytest import fixture


@fixture(scope="session")
def waypoints() -> Iterator[list[tuple[float, float]]]:
    with Path("tests/waypoints.csv").open("r") as file:
        data = reader(file, delimiter=",")
        next(data)  # skip header
        yield [(float(row[0]), float(row[1])) for row in data]
