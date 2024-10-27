# ruff: noqa

from cProfile import Profile as cProfile
from csv import reader
from pathlib import Path
from time import perf_counter_ns
from typing import Any, NamedTuple

from benchmarks.pycubicspline.pycubicspline import calc_2d_spline_interpolation
from scipath import Profile, create_cubic_path_2d


class BenchmarkResult(NamedTuple):
    timing: float
    meta: Any


def get_waypoints() -> list[tuple[float, float]]:
    with Path("tests/waypoints.csv").open("r") as file:
        data = reader(file, delimiter=",")
        next(data)  # skip header
        return [(float(row[0]), float(row[1])) for row in data]


def compute_pycubicspline(calls: int, x: list[float], y: list[float], number_of_points: int) -> BenchmarkResult:
    start = perf_counter_ns()

    for _ in range(calls):
        calc_2d_spline_interpolation(x, y, number_of_points)

    return BenchmarkResult(perf_counter_ns() - start, None)


def compute_scipath(calls: int, waypoints: list[tuple[float, float]]) -> BenchmarkResult:
    path_size = create_cubic_path_2d(waypoints, profile=Profile.ALL).path.size
    start = perf_counter_ns()

    for _ in range(calls):
        create_cubic_path_2d(waypoints, profile=Profile.ALL)

    return BenchmarkResult(perf_counter_ns() - start, path_size)


def main() -> None:
    waypoints = get_waypoints()
    x, y = list(zip(*waypoints))
    calls = 100
    scipath_result = compute_scipath(calls, waypoints)
    pycubicspline_result = compute_pycubicspline(calls, x, y, scipath_result.meta)

    profiler = cProfile()
    profiler.runcall(create_cubic_path_2d, waypoints, profile=Profile.ALL)
    profiler.print_stats()
    profiler.runcall(calc_2d_spline_interpolation, x, y, scipath_result.meta)  # pyright: ignore [reportUnknownArgumentType]
    profiler.print_stats()

    print(f"scipath: {scipath_result.timing / calls / 1_000_000:.6f} ms")
    print(f"pycubicspline: {pycubicspline_result.timing / calls / 1_000_000:.6f} ms")


if __name__ == "__main__":
    main()
