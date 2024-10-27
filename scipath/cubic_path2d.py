from __future__ import annotations

from collections.abc import Sequence
from enum import IntEnum
from typing import Any, Generic, Literal, Optional, TypeVar, overload

from numpy import arange, arctan2, concatenate, diff, floating, zeros
from numpy.linalg import norm
from numpy.typing import NDArray
from scipy.interpolate import CubicSpline
from typing_extensions import NamedTuple

FloatArray = NDArray[floating[Any]]
P_contra = TypeVar("P_contra", bound=Optional[FloatArray], contravariant=True)
Y_contra = TypeVar("Y_contra", bound=Optional[FloatArray], contravariant=True)
C_contra = TypeVar("C_contra", bound=Optional[FloatArray], contravariant=True)


class ConsecutiveDuplicateError(Exception):
    def __init__(self) -> None:
        super().__init__("Your input should not contain consecutive duplicate(s)!")


class CubicPath2D(NamedTuple, Generic[P_contra, Y_contra, C_contra]):
    path: P_contra
    yaw: Y_contra
    curvature: C_contra


class Profile(IntEnum):
    PATH = 0x001
    YAW = 0x010
    CURVATURE = 0x100
    NO_CURVATURE = 0x011
    NO_YAW = 0x101
    NO_PATH = 0x110
    ALL = 0x111


@overload
def create_cubic_path_2d(
    points: FloatArray | Sequence[tuple[float, float]],
    *,
    profile: Literal[Profile.PATH],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray, FloatArray | None, FloatArray | None]: ...
@overload
def create_cubic_path_2d(
    points: FloatArray | Sequence[tuple[float, float]],
    *,
    profile: Literal[Profile.YAW],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray | None, FloatArray, FloatArray | None]: ...
@overload
def create_cubic_path_2d(
    points: FloatArray | Sequence[tuple[float, float]],
    *,
    profile: Literal[Profile.CURVATURE],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray | None, FloatArray | None, FloatArray]: ...
@overload
def create_cubic_path_2d(
    points: FloatArray | Sequence[tuple[float, float]],
    *,
    profile: Literal[Profile.NO_CURVATURE],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray, FloatArray, FloatArray | None]: ...
@overload
def create_cubic_path_2d(
    points: FloatArray | Sequence[tuple[float, float]],
    *,
    profile: Literal[Profile.NO_YAW],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray, FloatArray | None, FloatArray]: ...
@overload
def create_cubic_path_2d(
    points: FloatArray | Sequence[tuple[float, float]],
    *,
    profile: Literal[Profile.NO_PATH],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray | None, FloatArray, FloatArray]: ...
@overload
def create_cubic_path_2d(
    points: FloatArray | Sequence[tuple[float, float]],
    *,
    profile: Literal[Profile.ALL],
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray, FloatArray, FloatArray]: ...
def create_cubic_path_2d(
    points: FloatArray | Sequence[tuple[float, float]],
    *,
    profile: Profile,
    distance_step: float = 0.05,
) -> CubicPath2D[FloatArray, FloatArray, FloatArray]:
    path = None
    yaw = None
    curvature = None
    first_derivative = None
    dx = None
    dy = None
    norms = concatenate((zeros(1), norm(diff(points, axis=0), axis=1).cumsum()))
    steps = arange(0, norms[-1], distance_step)

    try:
        cubic_spline = CubicSpline(norms, points, bc_type="natural")

    except ValueError as error:
        if diff(points, axis=0).any(axis=1).all():
            raise

        raise ConsecutiveDuplicateError from error

    if profile & Profile.PATH:
        path = cubic_spline(steps)

    if profile & Profile.YAW:
        first_derivative = cubic_spline.derivative(1)
        dx, dy = first_derivative(steps).T
        yaw = arctan2(dy, dx)  # pyright: ignore [reportUnknownArgumentType]

    if profile & Profile.CURVATURE:
        if yaw is None:
            first_derivative = cubic_spline.derivative()
            dx, dy = first_derivative(steps).T

        ddx, ddy = first_derivative.derivative()(steps).T  # pyright: ignore [reportOptionalMemberAccess]
        curvature = (dx * ddy - dy * ddx) / (dx * dx + dy * dy) ** 1.5  # pyright: ignore [reportOptionalOperand]

    return CubicPath2D(path, yaw, curvature)  # pyright: ignore [reportArgumentType, reportUnknownArgumentType]
