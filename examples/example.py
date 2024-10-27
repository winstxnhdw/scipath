from scipath import Profile, create_cubic_path_2d


def main() -> None:
    points = [(0, 0), (1, 1), (2, 0), (3, 1)]
    create_cubic_path_2d(points, profile=Profile.PATH)
    create_cubic_path_2d(points, profile=Profile.YAW)
    create_cubic_path_2d(points, profile=Profile.CURVATURE)
    create_cubic_path_2d(points, profile=Profile.NO_CURVATURE)
    create_cubic_path_2d(points, profile=Profile.NO_YAW)
    create_cubic_path_2d(points, profile=Profile.NO_PATH)


if __name__ == "__main__":
    main()
