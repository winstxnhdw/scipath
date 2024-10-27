# ruff: noqa

from scipath import Profile, create_cubic_path_2d


def test_profile_path(waypoints: list[tuple[float, float]]):
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.PATH)
    assert cubic_path.path is not None
    assert cubic_path.yaw is None
    assert cubic_path.curvature is None


def test_profile_yaw(waypoints: list[tuple[float, float]]):
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.YAW)
    assert cubic_path.path is None
    assert cubic_path.yaw.sum() == 17424.47461197635
    assert cubic_path.curvature is None


def test_profile_curvature(waypoints: list[tuple[float, float]]):
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.CURVATURE)
    assert cubic_path.path is None
    assert cubic_path.yaw is None
    assert cubic_path.curvature.sum() == 38.22376728677102


def test_profile_no_curvature(waypoints: list[tuple[float, float]]):
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.NO_CURVATURE)
    assert cubic_path.path is not None
    assert cubic_path.yaw.sum() == 17424.47461197635
    assert cubic_path.curvature is None


def test_profile_no_yaw(waypoints: list[tuple[float, float]]):
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.NO_YAW)
    assert cubic_path.path is not None
    assert cubic_path.yaw is None
    assert cubic_path.curvature.sum() == 38.22376728677102


def test_profile_no_path(waypoints: list[tuple[float, float]]):
    cubic_path = create_cubic_path_2d(waypoints, profile=Profile.NO_PATH)
    assert cubic_path.path is None
    assert cubic_path.yaw.sum() == 17424.47461197635
    assert cubic_path.curvature.sum() == 38.22376728677102
