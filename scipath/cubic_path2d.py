from __future__ import annotations

from collections.abc import Sequence
from enum import IntEnum
from logging import getLogger
from typing import Any, Generic, Literal, Union, overload

from numpy import arange, arctan2, bool_, concatenate, diff, dtype, floating, ndarray, zeros
from numpy.linalg import norm
from scipy.interpolate import CubicSpline
from typing_extensions import Never, TypedDict, TypeVar

FloatType = TypeVar("FloatType", bound=floating[Any])
Points = Union[ndarray[tuple[int, Literal[2]], dtype[FloatType]], Sequence[tuple[float, float]]]
FloatArray = ndarray[tuple[int], dtype[FloatType]]
BoolArray = ndarray[tuple[int], dtype[bool_]]
P = TypeVar("P", bound=FloatArray[floating[Any]])
Y = TypeVar("Y", bound=FloatArray[floating[Any]])
C = TypeVar("C", bound=FloatArray[floating[Any]])


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
    points: Points[floating[Any]],
    mask: BoolArray,
) -> None:
    duplicate_mask_with_previous = concatenate(([True], mask)) & concatenate((mask, [True]))
    highlighted_array = "\n".join(
        f"    \033[91m{row}\033[0m" if not duplicate_mask_with_previous[i] else f"    {row}"
        for i, row in enumerate(points)
    )

    logger = getLogger(__name__)
    logger.error("[")
    logger.error(highlighted_array)
    logger.error("]")


@overload
def create_cubic_path_2d(
    points: Points[FloatType],
    *,
    profile: Literal[Profile.PATH],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray[FloatType], Never, Never]: ...
@overload
def create_cubic_path_2d(
    points: Points[FloatType],
    *,
    profile: Literal[Profile.YAW],
    distance_step: float = 0.05,
) -> CubicPath2D[Never, FloatArray[FloatType], Never]: ...
@overload
def create_cubic_path_2d(
    points: Points[FloatType],
    *,
    profile: Literal[Profile.CURVATURE],
    distance_step: float = 0.05,
) -> CubicPath2D[Never, Never, FloatArray[FloatType]]: ...
@overload
def create_cubic_path_2d(
    points: Points[FloatType],
    *,
    profile: Literal[Profile.NO_CURVATURE],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray[FloatType], FloatArray[FloatType], Never]: ...
@overload
def create_cubic_path_2d(
    points: Points[FloatType],
    *,
    profile: Literal[Profile.NO_YAW],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray[FloatType], Never, FloatArray[FloatType]]: ...
@overload
def create_cubic_path_2d(
    points: Points[FloatType],
    *,
    profile: Literal[Profile.NO_PATH],
    distance_step: float = 0.05,
) -> CubicPath2D[Never, FloatArray[FloatType], FloatArray[FloatType]]: ...
@overload
def create_cubic_path_2d(
    points: Points[FloatType],
    *,
    profile: Literal[Profile.ALL],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray[FloatType], FloatArray[FloatType], FloatArray[FloatType]]: ...
def create_cubic_path_2d(
    points: Points[FloatType],
    *,
    profile: Profile,
    distance_step: float = 0.05,
) -> (
    CubicPath2D[FloatArray[FloatType], FloatArray[FloatType], FloatArray[FloatType]]
    | CubicPath2D[Never, FloatArray[FloatType], FloatArray[FloatType]]
    | CubicPath2D[FloatArray[FloatType], Never, FloatArray[FloatType]]
    | CubicPath2D[FloatArray[FloatType], FloatArray[FloatType], Never]
    | CubicPath2D[Never, Never, FloatArray[FloatType]]
    | CubicPath2D[Never, FloatArray[FloatType], Never]
    | CubicPath2D[FloatArray[FloatType], Never, Never]
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
        consecutive_duplicates_mask: BoolArray = diff(points, axis=0).any(axis=1)  # pyright: ignore[reportAssignmentType]

        if consecutive_duplicates_mask.all():
            raise

        highlight_consecutive_duplicates(points, consecutive_duplicates_mask)
        raise ConsecutiveDuplicateError from error

    if profile & Profile.PATH:
        cubic_path["path"] = cubic_spline(steps)

    if profile & Profile.YAW:
        first_derivative = cubic_spline.derivative(1)
        dx, dy = first_derivative(steps).T
        cubic_path["yaw"] = arctan2(dy, dx)  # pyright: ignore [reportUnknownArgumentType]

    if profile & Profile.CURVATURE:
        if first_derivative is None:
            first_derivative = cubic_spline.derivative()
            dx, dy = first_derivative(steps).T

        ddx, ddy = first_derivative.derivative()(steps).T
        cubic_path["curvature"] = (dx * ddy - dy * ddx) / (dx * dx + dy * dy) ** 1.5  # pyright: ignore [reportOptionalOperand]

    return cubic_path  # pyright: ignore [reportReturnType]
