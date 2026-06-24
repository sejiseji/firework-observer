from __future__ import annotations

from math import cos, sin


def rotate_2d(x: float, y: float, angle: float) -> tuple[float, float]:
    ca = cos(angle)
    sa = sin(angle)
    return x * ca - y * sa, x * sa + y * ca
