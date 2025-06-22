from pytest import raises

from scipath import Profile, create_cubic_path_2d
from scipath.cubic_path2d import ConsecutiveDuplicateError


def test_exception() -> None:
    invalid_waypoints = [(0, 0), (99, 1), (99, 1), (0, 4), (0, 1), (0, 1), (0, 3)]

    with raises(ConsecutiveDuplicateError):
        create_cubic_path_2d(invalid_waypoints, profile=Profile.ALL)
