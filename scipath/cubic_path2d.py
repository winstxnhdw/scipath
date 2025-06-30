from __future__ import annotations

from collections.abc import Sequence
from enum import IntEnum
from logging import ERROR, StreamHandler, getLogger
from typing import Any, Generic, Literal, TypeVar, overload

from numpy import arange, arctan2, bool_, concatenate, diff, dtype, floating, ndarray, zeros
from numpy.linalg import norm
from scipy.interpolate import CubicSpline
from typing_extensions import Never, TypedDict

FloatArray = ndarray[tuple[int, ...], dtype[floating[Any]]]
Points = FloatArray | Sequence[tuple[float, float]]
P = TypeVar("P", bound=FloatArray)
Y = TypeVar("Y", bound=FloatArray)
C = TypeVar("C", bound=FloatArray)


class ConsecutiveDuplicateError(Exception):
    def __init__(self) -> None:
        super().__init__("Your input should not contain consecutive duplicate(s)!")


class CubicPath2D(TypedDict, Generic[P, Y, C]):
    path: P
    yaw: Y
    curvature: C


class Profile(IntEnum):
    PATH = 0x001
    YAW = 0x010
    CURVATURE = 0x100
    NO_CURVATURE = 0x011
    NO_YAW = 0x101
    NO_PATH = 0x110
    ALL = 0x111


def highlight_consecutive_duplicates(
    points: Points,
    mask: ndarray[tuple[int, ...], dtype[bool_[bool]]],
) -> None:
    logger = getLogger(__name__)
    logger.setLevel(ERROR)
    logger.addHandler(StreamHandler())

    duplicate_mask_with_previous = concatenate(([True], mask)) & concatenate((mask, [True]))
    highlighted_array = "\n".join(
        f"    \033[91m{row}\033[0m" if not duplicate_mask_with_previous[i] else f"    {row}"
        for i, row in enumerate(points)
    )

    logger.error("[")
    logger.error(highlighted_array)
    logger.error("]")


@overload
def create_cubic_path_2d(
    points: Points,
    *,
    profile: Literal[Profile.PATH],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray, Never, Never]: ...
@overload
def create_cubic_path_2d(
    points: Points,
    *,
    profile: Literal[Profile.YAW],
    distance_step: float = 0.05,
) -> CubicPath2D[Never, FloatArray, Never]: ...
@overload
def create_cubic_path_2d(
    points: Points,
    *,
    profile: Literal[Profile.CURVATURE],
    distance_step: float = 0.05,
) -> CubicPath2D[Never, Never, FloatArray]: ...
@overload
def create_cubic_path_2d(
    points: Points,
    *,
    profile: Literal[Profile.NO_CURVATURE],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray, FloatArray, Never]: ...
@overload
def create_cubic_path_2d(
    points: Points,
    *,
    profile: Literal[Profile.NO_YAW],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray, Never, FloatArray]: ...
@overload
def create_cubic_path_2d(
    points: Points,
    *,
    profile: Literal[Profile.NO_PATH],
    distance_step: float = 0.05,
) -> CubicPath2D[Never, FloatArray, FloatArray]: ...
@overload
def create_cubic_path_2d(
    points: Points,
    *,
    profile: Literal[Profile.ALL],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray, FloatArray, FloatArray]: ...
def create_cubic_path_2d(
    points: Points,
    *,
    profile: Profile,
    distance_step: float = 0.05,
) -> (
    CubicPath2D[FloatArray, FloatArray, FloatArray]
    | CubicPath2D[Never, FloatArray, FloatArray]
    | CubicPath2D[FloatArray, Never, FloatArray]
    | CubicPath2D[FloatArray, FloatArray, Never]
    | CubicPath2D[Never, Never, FloatArray]
    | CubicPath2D[Never, FloatArray, Never]
    | CubicPath2D[FloatArray, Never, Never]
):
    cubic_path = {}
    first_derivative = None
    dx = None
    dy = None
    norms = concatenate((zeros(1), norm(diff(points, axis=0), axis=1).cumsum()))
    steps = arange(0, norms[-1], distance_step)

    try:
        cubic_spline = CubicSpline(norms, points, bc_type="natural")

    except ValueError as error:
        consecutive_duplicates_mask = diff(points, axis=0).any(axis=1)

        if consecutive_duplicates_mask.all():
            raise

        highlight_consecutive_duplicates(points, consecutive_duplicates_mask)  # pyright: ignore [reportUnknownArgumentType]
        raise ConsecutiveDuplicateError from error

    if profile & Profile.PATH:
        cubic_path["path"] = cubic_spline(steps)

    if profile & Profile.YAW:
        first_derivative = cubic_spline.derivative(1)
        dx, dy = first_derivative(steps).T
        cubic_path["yaw"] = arctan2(dy, dx)

    if profile & Profile.CURVATURE:
        if first_derivative is None:
            first_derivative = cubic_spline.derivative()
            dx, dy = first_derivative(steps).T

        ddx, ddy = first_derivative.derivative()(steps).T
        cubic_path["curvature"] = (dx * ddy - dy * ddx) / (dx * dx + dy * dy) ** 1.5  # pyright: ignore [reportOptionalOperand]

    return cubic_path  # pyright: ignore [reportReturnType]
