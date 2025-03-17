from typing import Literal

from scipath.cubic_path2d import FloatArray

def norm(
    x: FloatArray,
    ord: float | Literal["fro", "nuc"] | None = None,  # noqa: A002
    axis: int | tuple[int, int] | None = None,
    keepdims: bool = False,
) -> FloatArray: ...
