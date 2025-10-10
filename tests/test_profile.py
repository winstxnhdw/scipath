# ruff: noqa: S101
from __future__ import annotations

from scipath import Profile, create_cubic_path_2d


def test_profile_path(waypoints: list[tuple[float, float]]) -> None:
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.PATH)
    assert cubic_path.get("path") is not None
    assert cubic_path.get("yaw") is None
    assert cubic_path.get("curvature") is None


def test_profile_yaw(waypoints: list[tuple[float, float]]) -> None:
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.YAW)
    assert cubic_path.get("path") is None
    assert cubic_path.get("yaw") is not None
    assert cubic_path.get("curvature") is None


def test_profile_curvature(waypoints: list[tuple[float, float]]) -> None:
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.CURVATURE)
    assert cubic_path.get("path") is None
    assert cubic_path.get("yaw") is None
    assert cubic_path.get("curvature") is not None


def test_profile_no_curvature(waypoints: list[tuple[float, float]]) -> None:
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.NO_CURVATURE)
    assert cubic_path.get("path") is not None
    assert cubic_path.get("yaw") is not None
    assert cubic_path.get("curvature") is None


def test_profile_no_yaw(waypoints: list[tuple[float, float]]) -> None:
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.NO_YAW)
    assert cubic_path.get("path") is not None
    assert cubic_path.get("yaw") is None
    assert cubic_path.get("curvature") is not None


def test_profile_no_path(waypoints: list[tuple[float, float]]) -> None:
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.NO_PATH)
    assert cubic_path.get("path") is None
    assert cubic_path.get("yaw") is not None
    assert cubic_path.get("curvature") is not None
