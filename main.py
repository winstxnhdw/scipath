from csv import reader

from matplotlib import pyplot as plt

from cubic_spline_interpolator import (calculate_spline_curvature,
                                       calculate_spline_yaw,
                                       generate_cubic_path)


def main():
    """
    Summary
    -------
    Main function
    """
    with open('tests/waypoints.csv', newline='', encoding='utf-8') as file:
        rows = list(reader(file, delimiter=','))

    x, y = [[float(i) for i in row] for row in zip(*rows[1:])]

    spline_x, spline_y = generate_cubic_path(x, y)
    spline_yaw = calculate_spline_yaw(x, y)
    spline_curvature = calculate_spline_curvature(x, y)

    _, axes = plt.subplots(1, 3, figsize=(15, 5))
    plt.style.use('seaborn-pastel')

    axes[0].set_box_aspect(1)
    axes[0].set_title('Geometry')
    axes[0].plot(spline_x, spline_y, c='m')

    axes[1].set_box_aspect(1)
    axes[1].set_title('Yaw')
    axes[1].plot(spline_yaw, c='m')

    axes[2].set_box_aspect(1)
    axes[2].set_title('Curvature')
    axes[2].plot(spline_curvature, c='m')

    plt.show()


if __name__ == '__main__':
    main()
