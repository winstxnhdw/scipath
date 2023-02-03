import numpy as np
from numpy.typing import ArrayLike, NDArray
from scipy.interpolate import CubicSpline


def initialise_cubic_spline(x: ArrayLike, y: ArrayLike, distance_step: float, boundary_condition_type: str) -> tuple[CubicSpline, NDArray]:
    """
    Summary
    -------
    Initialises the cubic spline interpolator

    Parameters
    ----------
    x (ArrayLike): x coordinates of the waypoints
    y (ArrayLike): y coordinates of the waypoints
    distance_step (float): distance step between the waypoints
    boundary_condition_type (str): boundary condition type

    Returns
    -------
    cubic_spline (CubicSpline): cubic spline interpolator
    s (NDArray): distance coordinate of the cubic spline path
    """
    distances = np.concatenate((np.zeros(1), np.cumsum(np.hypot(np.ediff1d(x), np.ediff1d(y)))))
    points = np.array([x, y]).T
    s = np.arange(0, distances[-1], distance_step)

    try:
        cubic_spline = CubicSpline(distances, points, bc_type=boundary_condition_type, axis=0, extrapolate=False)

    except ValueError:
        print("If you are getting a sequence error, do check if your input dataset contains consecutive duplicate(s).")
        raise

    return cubic_spline, s


def generate_cubic_spline(x: ArrayLike, y: ArrayLike, distance_step: float=0.05, boundary_condition_type: str='natural') -> tuple[NDArray, ...]:
    """
    Summary
    -------
    Generates a cubic spline path with its yaw and curvature

    Parameters
    ----------
    x (ArrayLike): x coordinates of the waypoints
    y (ArrayLike): y coordinates of the waypoints
    distance_step (float): distance step between the waypoints
    boundary_condition_type (str): boundary condition type

    Returns
    -------
    spline_x (NDArray): x coordinates of the cubic spline path
    spline_y (NDArray): y coordinates of the cubic spline path
    yaw (NDArray): yaw of the cubic spline path
    curvature (ndarray): curvature of the cubic spline path
    """
    cubic_spline, s = initialise_cubic_spline(x, y, distance_step, boundary_condition_type)

    dx, dy = cubic_spline.derivative(1)(s).T
    yaw = np.arctan2(dy, dx)

    ddx, ddy = cubic_spline.derivative(2)(s).T
    curvature = (ddy*dx - ddx*dy) / ((dx*dx + dy*dy)**1.5)

    spline_x, spline_y = cubic_spline(s).T
    return spline_x, spline_y, yaw, curvature


def generate_cubic_path(x: ArrayLike, y: ArrayLike, distance_step: float=0.05, boundary_condition_type: str='natural') -> tuple[NDArray, NDArray]:
    """
    Summary
    -------
    Generates a cubic spline path

    Parameters
    ----------
    x (ArrayLike): x coordinates of the waypoints
    y (ArrayLike): y coordinates of the waypoints
    distance_step (float): distance step between the waypoints
    boundary_condition_type (str): boundary condition type

    Returns
    -------
    spline_x (ndarray): x coordinates of the cubic spline path
    spline_y (ndarray): y coordinates of the cubic spline path
    """
    cubic_spline, s = initialise_cubic_spline(x, y, distance_step, boundary_condition_type)
    spline_x, spline_y = cubic_spline(s).T

    return spline_x, spline_y


def calculate_spline_yaw(x: ArrayLike, y: ArrayLike, distance_step: float=0.05, boundary_condition_type: str='natural') -> NDArray:
    """
    Summary
    -------
    Calculates the yaw of a cubic spline path without generating the path

    Parameters
    ----------
    x (ArrayLike): x coordinates of the waypoints
    y (ArrayLike): y coordinates of the waypoints
    distance_step (float): distance step between the waypoints
    boundary_condition_type (str): boundary condition type

    Returns
    -------
    yaw (NDArray): yaw of the cubic spline path
    """
    cubic_spline, s = initialise_cubic_spline(x, y, distance_step, boundary_condition_type)
    dx, dy = cubic_spline.derivative(1)(s).T

    return np.arctan2(dy, dx)


def calculate_spline_curvature(x: ArrayLike, y: ArrayLike, distance_step: float=0.05, boundary_condition_type: str='natural') -> NDArray:
    """
    Summary
    -------
    Calculates the curvature of a cubic spline path without generating the path

    Parameters
    ----------
    x (ArrayLike): x coordinates of the waypoints
    y (ArrayLike): y coordinates of the waypoints

    Returns
    -------
    curvature (NDArray): curvature of the cubic spline path
    """
    cubic_spline, s = initialise_cubic_spline(x, y, distance_step, boundary_condition_type)
    first_derivative = cubic_spline.derivative(1)
    dx, dy = first_derivative(s).T
    ddx, ddy = first_derivative.derivative(1)(s).T

    return (ddy*dx - ddx*dy) / ((dx*dx + dy*dy)**1.5)
