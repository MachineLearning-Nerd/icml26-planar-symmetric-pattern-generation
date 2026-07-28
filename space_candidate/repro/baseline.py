"""Reconstruction of the exact checks visible in the judged Space."""

from __future__ import annotations

import math

import numpy as np

from repro import core


def claim_1(seed: int) -> dict:
    rng = np.random.default_rng(seed + 1)
    rows = []
    for name, (group, _) in core.POINT_GROUPS.items():
        recovered, supergroup_name = core.conjugation_check(name, rng)
        subgroup = all(
            core.is_in_group(matrix, core.REFLECTION_GROUPS[supergroup_name])
            for matrix in group
        )
        rows.append(
            {
                "group": name,
                "reflection_supergroup": supergroup_name,
                "conjugation_recovery": recovered,
                "point_group_subgroup": subgroup,
            }
        )
    passed = len(rows) == 17 and all(
        row["conjugation_recovery"] and row["point_group_subgroup"] for row in rows
    )
    return {
        "status": "VERIFIED" if passed else "BLOCKED",
        "source": "Theorem 3.2",
        "scope": "Complete finite classification of 17 planar point-group representatives; not a replacement for the abstract theorem proof.",
        "groups": rows,
    }


def claim_2_toy(seed: int) -> dict:
    rng = np.random.default_rng(seed + 2)
    group = core.POINT_GROUPS["p4mm"][0]
    points = rng.standard_normal((400, 2))
    weights = rng.standard_normal((8, 2))
    phases = rng.standard_normal(8)

    def rich(p: np.ndarray) -> np.ndarray:
        return np.sum(
            [np.cos(p @ weights[index] + phases[index]) for index in range(8)],
            axis=0,
        )

    target = core.orbit_average(rich, points, group)
    candidate_bases = []
    for kx in np.linspace(-3, 3, 9):
        for ky in np.linspace(-3, 3, 9):
            if kx == 0 and ky == 0:
                continue
            frequency = np.array([kx, ky])
            candidate_bases.append(
                core.orbit_average(
                    lambda p, k=frequency: np.cos(p @ k), points, group
                )
            )
    errors = {}
    for rank in (4, 8, 16, 32, 64):
        design = np.asarray(candidate_bases[:rank]).T
        coefficient, *_ = np.linalg.lstsq(design, target, rcond=None)
        errors[str(rank)] = float(
            np.sqrt(np.mean(np.square(design @ coefficient - target)))
        )
    corroborates = errors["32"] < errors["4"] / 3 and errors["32"] < 0.3
    return {
        "status": "BLOCKED",
        "judge_baseline_category": "TOY",
        "source": "Theorem 3.3",
        "finite_corroboration_pass": corroborates,
        "rmse_by_basis_count": errors,
        "reason": "One finite p4mm target cannot establish the theorem's universal quantifiers.",
    }


def claim_3(seed: int) -> dict:
    rng = np.random.default_rng(seed + 3)
    errors = {
        name: core.decomposition_invariance(name, rng)
        for name in core.POINT_GROUPS
    }
    maximum = max(errors.values())
    return {
        "status": "VERIFIED" if maximum < 1e-9 else "BLOCKED",
        "source": "Equation 3",
        "max_invariance_error": maximum,
        "errors": errors,
    }


def claim_4(seed: int) -> dict:
    rng = np.random.default_rng(seed + 4)
    errors = {
        name: core.generated_pattern_error(name, rng)
        for name in core.POINT_GROUPS
    }
    maximum = max(errors.values())
    return {
        "status": "VERIFIED" if maximum < 1e-9 else "BLOCKED",
        "source": "Algorithm 1 and Section 6.1",
        "max_symmetry_error": maximum,
        "errors": errors,
    }


def claim_6_toy(seed: int) -> dict:
    rng = np.random.default_rng(seed + 6)

    def rotation3(axis: np.ndarray, angle: float) -> np.ndarray:
        axis = axis / np.linalg.norm(axis)
        cosine, sine = math.cos(angle), math.sin(angle)
        cross = np.array(
            [
                [0.0, -axis[2], axis[1]],
                [axis[2], 0.0, -axis[0]],
                [-axis[1], axis[0], 0.0],
            ]
        )
        return np.eye(3) + sine * cross + (1.0 - cosine) * (cross @ cross)

    generators = [
        rotation3(np.array([1.0, 0.0, 0.0]), math.pi / 2),
        rotation3(np.array([0.0, 1.0, 0.0]), math.pi / 2),
        rotation3(np.array([0.0, 0.0, 1.0]), math.pi / 2),
    ]

    def closure(initial: list[np.ndarray], gens: list[np.ndarray]) -> list[np.ndarray]:
        result = list(initial)
        changed = True
        while changed:
            changed = False
            for left in list(result):
                for right in gens:
                    product = left @ right
                    if not any(np.max(np.abs(product - item)) < 1e-7 for item in result):
                        result.append(product)
                        changed = True
        return result

    rotations = closure([np.eye(3)], generators)
    reflections = closure(
        rotations,
        [
            np.diag([-1.0, 1.0, 1.0]),
            np.diag([1.0, -1.0, 1.0]),
            np.diag([1.0, 1.0, -1.0]),
        ],
    )
    candidate = rng.standard_normal((3, 3))
    while abs(np.linalg.det(candidate)) < 0.3:
        candidate = rng.standard_normal((3, 3))
    inverse = np.linalg.inv(candidate)
    recovery = all(
        any(
            np.max(
                np.abs(
                    inverse @ (candidate @ matrix @ inverse) @ candidate - target
                )
            )
            < 1e-7
            for target in reflections
        )
        for matrix in rotations
    )
    return {
        "status": "BLOCKED",
        "judge_baseline_category": "TOY",
        "source": "Theorem B.9 only",
        "octahedral_rotation_group_size": len(rotations),
        "octahedral_reflection_group_size": len(reflections),
        "conjugation_recovery": recovery,
        "reason": "This does not test topology optimization, homogenization, or zero-shot metamaterial design.",
    }


def run_baseline(seed: int) -> dict:
    c1 = claim_1(seed)
    c2 = claim_2_toy(seed)
    c3 = claim_3(seed)
    c4 = claim_4(seed)
    c6 = claim_6_toy(seed)

    wrong_subgroup = all(
        core.is_in_group(matrix, core.REFLECTION_GROUPS["D4"])
        for matrix in core.POINT_GROUPS["p6"][0]
    )
    rng = np.random.default_rng(seed + 90)
    broken_decomposition_error = core.decomposition_invariance(
        "p4", rng, invariant_coefficients=False
    )
    broken_pattern_error = core.generated_pattern_error(
        "p4", rng, orbit_averaged=False
    )
    controls = {
        "wrong_p6_subgroup_of_D4": {
            "observed": wrong_subgroup,
            "expected": False,
            "passes": not wrong_subgroup,
        },
        "noninvariant_coefficients": {
            "observed_error": broken_decomposition_error,
            "expected_minimum": 1e-3,
            "passes": broken_decomposition_error > 1e-3,
        },
        "no_orbit_average": {
            "observed_error": broken_pattern_error,
            "expected_minimum": 1e-3,
            "passes": broken_pattern_error > 1e-3,
        },
        "uap_low_rank_is_worse": {
            "observed": c2["rmse_by_basis_count"]["4"]
            > c2["rmse_by_basis_count"]["32"],
            "expected": True,
            "passes": c2["rmse_by_basis_count"]["4"]
            > c2["rmse_by_basis_count"]["32"],
        },
        "octahedral_rotations_are_not_full_reflection_group": {
            "observed": c6["octahedral_rotation_group_size"]
            != c6["octahedral_reflection_group_size"],
            "expected": True,
            "passes": c6["octahedral_rotation_group_size"]
            != c6["octahedral_reflection_group_size"],
        },
    }
    if not all(control["passes"] for control in controls.values()):
        raise RuntimeError(f"negative control did not behave as intended: {controls}")
    return {
        "claims": {
            "claim_1": c1,
            "claim_2": c2,
            "claim_3": c3,
            "claim_4": c4,
            "claim_5": {
                "status": "BLOCKED",
                "judge_baseline_category": "INCONCLUSIVE",
                "reason": "No VTM experiment in the judged baseline.",
            },
            "claim_6": c6,
        },
        "negative_controls": controls,
    }
