# ruff: noqa: S101

from __future__ import annotations

from math import isclose

from scipath import Profile, create_cubic_path_2d


def test_regression(waypoints: list[tuple[float, float]]) -> None:
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.ALL)
    assert isclose(cubic_path["yaw"].sum(), 17424.47461197635)
    assert isclose(cubic_path["curvature"].sum(), 38.22376728677102)
