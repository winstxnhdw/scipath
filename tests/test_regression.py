# ruff: noqa

from scipath import Profile, create_cubic_path_2d


def test_regression(waypoints: list[tuple[float, float]]) -> None:
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.ALL)
    assert cubic_path.yaw.mean() == 1.3113926854802702
    assert cubic_path.curvature.mean() == 0.0028767793547656373
