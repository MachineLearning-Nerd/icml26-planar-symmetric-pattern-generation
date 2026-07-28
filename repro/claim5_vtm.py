"""Paper-native Virtual Temperature Method audit for Claim 5.

The released solver is fetched from an immutable upstream commit and verified
byte-for-byte before import.  The test uses the 128x128 mesh specified in
Appendix F.2, formed by tiling a 64x64 p4mm unit cell into the required 2x2
supercell.
"""

from __future__ import annotations

import hashlib
import importlib
import math
import sys
import urllib.request
import warnings
from collections import deque
from pathlib import Path

import numpy as np
import torch


ROOT = Path(__file__).resolve().parents[1]
UPSTREAM_COMMIT = "b6a27efef00b80923ce9e6b66bb8847e83f289cf"
UPSTREAM_REPOSITORY = "https://github.com/GLAD-RUC/Sym2D"
UPSTREAM_FILES = {
    "topology/fea_base.py": "a5108647f928a4b9c0804971fb13d2f8a852eb3c10d07eb6d2cfccb314427641",
    "topology/vtm.py": "6af06aeacd1260c9680ca1d6eee12a11213125d5eafc4fd85f92ebb33ddbab48",
}
PAPER_SOURCE_SHA256 = (
    "0d9de93e9af7441ac803837bf4bebceed7d890b015ea4c194bad5dd414921d55"
)
SIZE = 128
UNIT = 64
SINK_LENGTH = 64


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _load_pinned_solver():
    cache = ROOT / ".openresearch" / "runtime_cache" / f"sym2d-{UPSTREAM_COMMIT}"
    for relative, expected_hash in UPSTREAM_FILES.items():
        destination = cache / relative
        if destination.exists() and _sha256(destination.read_bytes()) == expected_hash:
            continue
        url = (
            "https://raw.githubusercontent.com/GLAD-RUC/Sym2D/"
            f"{UPSTREAM_COMMIT}/{relative}"
        )
        request = urllib.request.Request(
            url, headers={"User-Agent": "OpenResearch-reproduction/1.0"}
        )
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
        observed_hash = _sha256(data)
        if observed_hash != expected_hash:
            raise RuntimeError(
                f"Upstream source hash mismatch for {relative}: "
                f"{observed_hash} != {expected_hash}"
            )
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
    init = cache / "topology" / "__init__.py"
    init.touch(exist_ok=True)
    sys.path.insert(0, str(cache))
    importlib.invalidate_caches()
    from topology.vtm import ObliqueElemVTM

    return ObliqueElemVTM


def _unit_designs() -> tuple[np.ndarray, np.ndarray]:
    coordinates = np.arange(UNIT, dtype=float) - (UNIT - 1) / 2
    yy, xx = np.meshgrid(coordinates, coordinates, indexing="ij")
    island_material = (np.maximum(np.abs(xx), np.abs(yy)) <= 10.5)
    connected_material = (np.abs(xx) <= 4.5) | (np.abs(yy) <= 4.5)
    island = np.where(island_material, 1.0, 0.05).astype(np.float32)
    connected = np.where(connected_material, 1.0, 0.05).astype(np.float32)
    return connected, island


def _tile_2x2(unit_cell: np.ndarray) -> np.ndarray:
    return np.tile(unit_cell, (2, 2))


def _symmetry_errors(density: np.ndarray) -> dict[str, float]:
    unit = density[:UNIT, :UNIT]
    operations = [
        np.rot90(unit, k=1),
        np.rot90(unit, k=2),
        np.rot90(unit, k=3),
        np.flipud(unit),
        np.fliplr(unit),
        unit.T,
        np.flipud(np.fliplr(unit.T)),
    ]
    return {
        "p4mm_D4_max_abs_error": float(
            max(np.max(np.abs(unit - transformed)) for transformed in operations)
        ),
        "translation_a_max_abs_error": float(
            np.max(np.abs(density - np.roll(density, UNIT, axis=1)))
        ),
        "translation_b_max_abs_error": float(
            np.max(np.abs(density - np.roll(density, UNIT, axis=0)))
        ),
    }


def _unreachable_material_cells(density: np.ndarray) -> int:
    """Four-neighbour flood fill from the paper's Γ boundary segments."""

    material = density > 0.5
    seen = np.zeros_like(material, dtype=bool)
    queue: deque[tuple[int, int]] = deque()
    # Γ = {0}x[0,1) union [0,1)x{0} in the 2x2 supercell coordinates.
    for index in range(SINK_LENGTH):
        for cell in ((index, 0), (0, index)):
            if material[cell] and not seen[cell]:
                seen[cell] = True
                queue.append(cell)
    while queue:
        row, column = queue.popleft()
        for next_row, next_column in (
            (row - 1, column),
            (row + 1, column),
            (row, column - 1),
            (row, column + 1),
        ):
            if (
                0 <= next_row < SIZE
                and 0 <= next_column < SIZE
                and material[next_row, next_column]
                and not seen[next_row, next_column]
            ):
                seen[next_row, next_column] = True
                queue.append((next_row, next_column))
    return int(np.count_nonzero(material & ~seen))


def _solver_kwargs() -> dict:
    return {
        "nelx": SIZE,
        "nely": SIZE,
        "a": UNIT,
        "b": UNIT,
        "gamma": math.pi / 2,
        "phi": 0.0,
        "task": "cycle_ab",
        "q0": 1e-4,
        "k0": 1.0,
        "penal": 5.0,
        "pp": 20,
        "device": torch.device("cpu"),
        "Eeps": 1e-4,
    }


def _native_measurement(solver_class, density: torch.Tensor) -> tuple[dict, object]:
    solver = solver_class(**_solver_kwargs())
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        surrogate, score, temperature = solver.vtm_loss(density, maxiter=500)
    x = density.detach().cpu().numpy()
    stiffness, rhs = solver.get_K_and_rhs(x)
    free_temperature = solver.t[solver.free]
    residual = stiffness @ free_temperature - rhs
    relative_residual = float(
        np.linalg.norm(residual) / max(np.linalg.norm(rhs), np.finfo(float).eps)
    )
    independently_recomputed_score = float(
        (np.sum(solver.t**solver.pp) / solver.ndof) ** (1 / solver.pp)
    )
    result = {
        "p20_temperature_score": float(score),
        "independently_recomputed_score": independently_recomputed_score,
        "score_recomputation_abs_error": abs(
            float(score) - independently_recomputed_score
        ),
        "temperature_max": float(np.max(temperature)),
        "temperature_mean": float(np.mean(temperature)),
        "linear_system_relative_residual": relative_residual,
        "surrogate_loss": float(surrogate),
        "finite": bool(
            np.isfinite(temperature).all()
            and math.isfinite(float(score))
            and torch.isfinite(surrogate)
        ),
        "warning_count": len(caught),
    }
    return result, solver


def _checker(
    connected: np.ndarray,
    island: np.ndarray,
    measurements: dict,
    descent: dict,
) -> tuple[bool, list[dict]]:
    connected_symmetry = _symmetry_errors(connected)
    island_symmetry = _symmetry_errors(island)
    connected_unreachable = _unreachable_material_cells(connected)
    island_unreachable = _unreachable_material_cells(island)
    checks: list[dict] = []

    def add(name: str, passed: bool, detail: object) -> None:
        checks.append({"name": name, "passed": bool(passed), "detail": detail})

    add("paper_mesh_128x128", connected.shape == (128, 128), connected.shape)
    add(
        "two_by_two_periodic_supercell",
        all(
            error == 0.0
            for error in (
                connected_symmetry["translation_a_max_abs_error"],
                connected_symmetry["translation_b_max_abs_error"],
                island_symmetry["translation_a_max_abs_error"],
                island_symmetry["translation_b_max_abs_error"],
            )
        ),
        {"connected": connected_symmetry, "island": island_symmetry},
    )
    add(
        "p4mm_symmetry_preserved",
        connected_symmetry["p4mm_D4_max_abs_error"] == 0.0
        and island_symmetry["p4mm_D4_max_abs_error"] == 0.0,
        {"connected": connected_symmetry, "island": island_symmetry},
    )
    add(
        "independent_flood_fill_oracle",
        connected_unreachable == 0 and island_unreachable > 0,
        {
            "connected_unreachable_material_cells": connected_unreachable,
            "island_unreachable_material_cells": island_unreachable,
        },
    )
    add(
        "native_scores_finite",
        measurements["connected"]["finite"] and measurements["island"]["finite"],
        measurements,
    )
    add(
        "island_is_hotter_than_connected",
        measurements["island"]["p20_temperature_score"]
        > 2.0 * measurements["connected"]["p20_temperature_score"],
        {
            "ratio": measurements["island"]["p20_temperature_score"]
            / measurements["connected"]["p20_temperature_score"]
        },
    )
    add(
        "independent_score_recomputation",
        max(
            measurements[name]["score_recomputation_abs_error"]
            for name in ("connected", "island")
        )
        < 1e-10,
        {
            name: measurements[name]["score_recomputation_abs_error"]
            for name in ("connected", "island")
        },
    )
    add(
        "linear_system_residual",
        max(
            measurements[name]["linear_system_relative_residual"]
            for name in ("connected", "island")
        )
        < 5e-5,
        {
            name: measurements[name]["linear_system_relative_residual"]
            for name in ("connected", "island")
        },
    )
    add(
        "released_adjoint_descent",
        descent["gradient_finite"]
        and descent["score_after"] < descent["score_before"],
        descent,
    )
    return all(row["passed"] for row in checks), checks


def verify_claim_5(config: dict) -> tuple[dict, dict]:
    if config["stage"] != "claim5_vtm_128":
        raise RuntimeError(f"Unsupported Claim 5 stage: {config['stage']}")
    torch.set_num_threads(min(8, max(1, int(config["estimated_scientific_cores"]))))
    solver_class = _load_pinned_solver()
    connected_unit, island_unit = _unit_designs()
    connected = _tile_2x2(connected_unit)
    island = _tile_2x2(island_unit)
    connected_tensor = torch.from_numpy(connected)
    island_tensor = torch.from_numpy(island)

    connected_measurement, _ = _native_measurement(
        solver_class, connected_tensor
    )
    island_measurement, _ = _native_measurement(solver_class, island_tensor)
    measurements = {
        "connected": connected_measurement,
        "island": island_measurement,
    }

    differentiable_island = island_tensor.clone().requires_grad_(True)
    before_measurement, _ = _native_measurement(
        solver_class, differentiable_island
    )
    # Use the native public API for the differentiable path and adjoint gradient.
    native_solver = solver_class(**_solver_kwargs())
    native_loss, score_before, _ = native_solver.vtm_loss(
        differentiable_island, maxiter=500
    )
    native_loss.backward()
    gradient = differentiable_island.grad.detach()
    stepped = (differentiable_island.detach() - 0.01 * gradient).clamp(0.05, 1.0)
    after_measurement, _ = _native_measurement(solver_class, stepped)
    descent = {
        "fixed_step_size": 0.01,
        "score_before": float(score_before),
        "score_after": after_measurement["p20_temperature_score"],
        "absolute_reduction": float(score_before)
        - after_measurement["p20_temperature_score"],
        "relative_reduction": (
            float(score_before) - after_measurement["p20_temperature_score"]
        )
        / float(score_before),
        "gradient_l2": float(torch.linalg.vector_norm(gradient)),
        "gradient_finite": bool(torch.isfinite(gradient).all()),
        "native_surrogate_loss": float(native_loss),
        "independent_before_replay_score": before_measurement[
            "p20_temperature_score"
        ],
    }

    passed, checks = _checker(connected, island, measurements, descent)

    broken_periodicity = island.copy()
    broken_periodicity[0, 0] = 1.0
    broken_symmetry = island.copy()
    broken_symmetry[13, 19] = 1.0
    controls = {
        "disconnected_periodic_islands_fail_connectivity": {
            "passes": _unreachable_material_cells(island) > 0,
            "unreachable_material_cells": _unreachable_material_cells(island),
        },
        "single_pixel_periodicity_break_rejected": {
            "passes": _symmetry_errors(broken_periodicity)[
                "translation_a_max_abs_error"
            ]
            > 0,
            "errors": _symmetry_errors(broken_periodicity),
        },
        "single_pixel_p4mm_break_rejected": {
            "passes": _symmetry_errors(broken_symmetry)["p4mm_D4_max_abs_error"]
            > 0,
            "errors": _symmetry_errors(broken_symmetry),
        },
    }
    all_controls = all(item["passes"] for item in controls.values())
    verdict = passed and all_controls
    result = {
        "status": "VERIFIED" if verdict else "BLOCKED",
        "source": "Section 6.2, Equation 6, Figure 4, Appendix E.3 and F.2",
        "evidence_type": "paper-native 128x128 finite-element VTM with independent oracles",
        "paper_source_sha256": PAPER_SOURCE_SHA256,
        "official_release": {
            "repository": UPSTREAM_REPOSITORY,
            "commit": UPSTREAM_COMMIT,
            "files_sha256": UPSTREAM_FILES,
        },
        "configuration": {
            "mesh": [128, 128],
            "unit_cell": [64, 64],
            "supercell": "2x2",
            "group": "p4mm",
            "sink_gamma": "{0}x[0,1) union [0,1)x{0}",
            "q0": 1e-4,
            "conductivity_range": [1e-4, 1.0],
            "simp_penalty": 5.0,
            "p_norm": 20,
            "max_cg_iterations": 500,
        },
        "measurements": measurements,
        "descent": descent,
        "checks": checks,
        "all_checks_pass": passed,
        "all_negative_controls_pass": all_controls,
        "limitations": (
            "This verifies the released VTM mechanism, its adjoint descent, "
            "the paper-specified mesh, and the theorem premises on constructed "
            "periodic p4mm designs. It does not reproduce diffusion-guided "
            "image generation, fabricate a paper cutout, or establish that "
            "every optimizer trajectory reaches a connected design."
        ),
    }
    if not verdict:
        raise RuntimeError(f"Claim 5 VTM verification failed: {result}; {controls}")
    return result, controls
