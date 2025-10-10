from cProfile import Profile as cProfile
from csv import reader
from pathlib import Path
from time import perf_counter_ns
from typing import Any, Literal, NamedTuple, Tuple

from numpy import array, dtype, float64, floating, ndarray

from benchmarks.pycubicspline.pycubicspline import (  # pyright: ignore [reportMissingModuleSource]
    calc_2d_spline_interpolation,
)
from scipath import FloatArray, Profile, create_cubic_path_2d

Points = ndarray[Tuple[int, Literal[2]], dtype[floating[Any]]]


class BenchmarkResult(NamedTuple):
    timing: float
    meta: Any


def get_waypoints() -> Points:
    with Path("tests/waypoints.csv").open("r") as file:
        data = reader(file, delimiter=",")
        next(data)  # skip header
        return array([(float(row[0]), float(row[1])) for row in data])  # pyright: ignore[reportReturnType]


def compute_pycubicspline(
    calls: int,
    x: FloatArray[float64],
    y: FloatArray[float64],
    number_of_points: int,
) -> BenchmarkResult:
    start = perf_counter_ns()

    for _ in range(calls):
        calc_2d_spline_interpolation(x, y, number_of_points)

    return BenchmarkResult(perf_counter_ns() - start, None)


def compute_scipath(calls: int, waypoints: Points) -> BenchmarkResult:
    path_size = create_cubic_path_2d(waypoints, profile=Profile.ALL)["path"].size
    start = perf_counter_ns()

    for _ in range(calls):
        create_cubic_path_2d(waypoints, profile=Profile.ALL)

    return BenchmarkResult(perf_counter_ns() - start, path_size)


def main() -> None:
    waypoints = get_waypoints()
    x, y = waypoints.T
    calls = 100
    scipath_result = compute_scipath(calls, waypoints)
    pycubicspline_result = compute_pycubicspline(calls, x, y, scipath_result.meta)  # pyright: ignore[reportArgumentType]

    profiler = cProfile()
    profiler.runcall(create_cubic_path_2d, waypoints, profile=Profile.ALL)
    profiler.print_stats()
    profiler.runcall(calc_2d_spline_interpolation, x, y, scipath_result.meta)  # pyright: ignore[reportUnknownArgumentType]
    profiler.print_stats()

    print(f"scipath: {scipath_result.timing / calls / 1_000_000:.6f} ms")  # noqa: T201
    print(f"pycubicspline: {pycubicspline_result.timing / calls / 1_000_000:.6f} ms")  # noqa: T201


if __name__ == "__main__":
    main()
