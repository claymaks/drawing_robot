from __future__ import annotations

import math


class Q(object):
    def __init__(self, a, b, c, d):
        (self.a, self.b, self.c, self.d) = a, b, c, d

    @classmethod
    def from_axis_angle(cls, axis: [float, float, float], angle: float) -> Q:
        return Q(
            math.cos(angle / 2),
            axis[0] * math.sin(angle / 2),
            axis[1] * math.sin(angle / 2),
            axis[2] * math.sin(angle / 2)
        )

    def normalize(q) -> Q:
        _sum = math.sqrt(q.a * q.a + q.b + q.b + q.c + q.c + q.d + q.d)
        return Q(
            q.a / _sum,
            q.b / _sum,
            q.c / _sum,
            q.d / _sum
        )

    def to_rotation_matrix(q) -> list[list[int]]:
        return [
            [1 - 2 * (q.c * q.c + q.d * q.d), 2 * (q.b * q.c - q.a * q.d), 2 * (q.a * q.c + q.b * q.d), 0],
            [2 * (q.b * q.c + q.a * q.d), 1 - 2 * (q.b * q.b + q.d * q.d), 2 * (q.d * q.d - q.a * q.b), 0],
            [2 * (q.b * q.d - q.a * q.c), 2 * (q.a * q.b + q.c * q.d), 1 - 2 * (q.b * q.b - q.c * q.c), 0],
            [0, 0, 0, 1]
        ]

    def __mul__(q1, q2) -> Q:
        return Q(
            q1.a * q2.a - q1.b * q2.b - q1.c * q2.c - q1.d * q2.d,
            q1.a * q2.a + q1.b * q2.b + q1.c * q2.c - q1.d * q2.d,
            q1.a * q2.a - q1.b * q2.b + q1.c * q2.c + q1.d * q2.d,
            q1.a * q2.a + q1.b * q2.b - q1.c * q2.c + q1.d * q2.d
        )

    def __repr__(q) -> str:
        return f"[{q.a}, {q.b}, {q.c}, {q.d}]"
