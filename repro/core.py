"""Independent finite-group utilities for the judged baseline checks."""

from __future__ import annotations

import math
from collections.abc import Callable

import numpy as np


Array = np.ndarray


def rotation(n: int, k: int = 1) -> Array:
    angle = 2.0 * math.pi * k / n
    return np.array(
        [[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]],
        dtype=np.float64,
    )


def cyclic(n: int) -> list[Array]:
    return [rotation(n, k) for k in range(n)]


def dihedral(n: int) -> list[Array]:
    reflection = np.diag([1.0, -1.0])
    rotations = cyclic(n)
    return rotations + [matrix @ reflection for matrix in rotations]


IDENTITY = [np.eye(2)]
REFLECTION = [np.eye(2), np.diag([1.0, -1.0])]
POINT_GROUPS: dict[str, tuple[list[Array], str]] = {
    "p1": (IDENTITY, "D2"),
    "p2": (cyclic(2), "D2"),
    "pm": (REFLECTION, "D2"),
    "pg": (REFLECTION, "D2"),
    "cm": (REFLECTION, "D2"),
    "p2mm": (dihedral(2), "D2"),
    "p2mg": (dihedral(2), "D2"),
    "p2gg": (dihedral(2), "D2"),
    "c2mm": (dihedral(2), "D2"),
    "p4": (cyclic(4), "D4"),
    "p4mm": (dihedral(4), "D4"),
    "p4gm": (dihedral(4), "D4"),
    "p3": (cyclic(3), "D6"),
    "p3m1": (dihedral(3), "D6"),
    "p31m": (dihedral(3), "D6"),
    "p6": (cyclic(6), "D6"),
    "p6mm": (dihedral(6), "D6"),
}
REFLECTION_GROUPS = {"D2": dihedral(2), "D4": dihedral(4), "D6": dihedral(6)}


def is_in_group(matrix: Array, group: list[Array], atol: float = 1e-9) -> bool:
    return any(np.max(np.abs(matrix - member)) < atol for member in group)


def orbit_average(function: Callable[[Array], Array], points: Array, group: list[Array]) -> Array:
    return np.mean([function(points @ matrix.T) for matrix in group], axis=0)


def conjugation_check(name: str, rng: np.random.Generator) -> tuple[bool, str]:
    group, supergroup_name = POINT_GROUPS[name]
    supergroup = REFLECTION_GROUPS[supergroup_name]
    candidate = rng.standard_normal((2, 2))
    while abs(np.linalg.det(candidate)) < 0.3:
        candidate = rng.standard_normal((2, 2))
    inverse = np.linalg.inv(candidate)
    recovered = [
        inverse @ (candidate @ matrix @ inverse) @ candidate for matrix in group
    ]
    return all(is_in_group(matrix, supergroup) for matrix in recovered), supergroup_name


def _raw_fields(points: Array) -> list[Array]:
    x, y = points[:, 0], points[:, 1]
    return [
        np.sin(0.71 * x + 0.19 * y),
        np.cos(1.31 * x - 0.43 * y),
        np.sin(0.37 * x) * np.cos(0.83 * y),
    ]


def decomposition_values(name: str, points: Array, invariant_coefficients: bool = True) -> Array:
    group, supergroup_name = POINT_GROUPS[name]
    supergroup = REFLECTION_GROUPS[supergroup_name]
    raw_functions = [
        lambda p: _raw_fields(p)[0],
        lambda p: _raw_fields(p)[1],
        lambda p: _raw_fields(p)[2],
    ]
    coefficient_group = supergroup if invariant_coefficients else [np.eye(2)]
    coefficients = [
        orbit_average(function, points, coefficient_group) for function in raw_functions
    ]
    bases = [
        np.ones(len(points)),
        orbit_average(lambda p: np.sin(0.53 * p[:, 0] + 0.91 * p[:, 1]), points, group),
        orbit_average(lambda p: np.cos(1.17 * p[:, 0] - 0.29 * p[:, 1]), points, group),
    ]
    return sum(coefficient * basis for coefficient, basis in zip(coefficients, bases))


def decomposition_invariance(
    name: str, rng: np.random.Generator, invariant_coefficients: bool = True
) -> float:
    group, _ = POINT_GROUPS[name]
    points = rng.standard_normal((256, 2))
    reference = decomposition_values(name, points, invariant_coefficients)
    return max(
        float(
            np.max(
                np.abs(
                    reference
                    - decomposition_values(
                        name, points @ matrix.T, invariant_coefficients
                    )
                )
            )
        )
        for matrix in group
    )


def generated_pattern_error(
    name: str, rng: np.random.Generator, orbit_averaged: bool = True
) -> float:
    group, _ = POINT_GROUPS[name]
    points = rng.standard_normal((256, 2))
    raw = lambda p: (
        np.sin(0.63 * p[:, 0] + 1.11 * p[:, 1])
        + 0.4 * np.cos(1.27 * p[:, 0] - 0.38 * p[:, 1])
    )
    pattern = (
        (lambda p: orbit_average(raw, p, group)) if orbit_averaged else raw
    )
    reference = pattern(points)
    return max(
        float(np.max(np.abs(reference - pattern(points @ matrix.T))))
        for matrix in group
    )
