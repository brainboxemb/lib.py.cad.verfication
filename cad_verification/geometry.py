"""Generic mesh geometry verification."""

from __future__ import annotations

from dataclasses import dataclass
import math
from numbers import Real
from pathlib import Path
from typing import Any, Iterable

import trimesh

from .errors import MeshLoadError, VerificationConfigError, VerificationFailure


def _number(value: Any, name: str) -> float:
    """Return one finite real number or raise a configuration error."""

    if isinstance(value, bool) or not isinstance(value, Real):
        raise VerificationConfigError(f"{name} must be a number")
    result = float(value)
    if not math.isfinite(result):
        raise VerificationConfigError(f"{name} must be finite")
    return result


def _non_negative(value: Any, name: str) -> float:
    """Return one finite non-negative number."""

    result = _number(value, name)
    if result < 0:
        raise VerificationConfigError(f"{name} may not be negative")
    return result


def _xyz(value: Iterable[Any], name: str) -> tuple[float, float, float]:
    """Normalize one three-value XYZ vector."""

    try:
        values = tuple(value)
    except TypeError as exc:
        raise VerificationConfigError(
            f"{name} must contain exactly three numbers"
        ) from exc
    if len(values) != 3:
        raise VerificationConfigError(
            f"{name} must contain exactly three numbers"
        )
    return (
        _number(values[0], f"{name}[0]"),
        _number(values[1], f"{name}[1]"),
        _number(values[2], f"{name}[2]"),
    )


@dataclass(frozen=True)
class SurfaceDistanceProbe:
    """One nearest-surface distance expectation."""

    label: str
    point: tuple[float, float, float]
    distance_mm: float
    tolerance_mm: float

    def __post_init__(self) -> None:
        label = str(self.label).strip()
        if not label:
            raise VerificationConfigError("probe label may not be empty")
        object.__setattr__(self, "label", label)
        object.__setattr__(self, "point", _xyz(self.point, "probe point"))
        object.__setattr__(
            self,
            "distance_mm",
            _non_negative(self.distance_mm, "probe distance_mm"),
        )
        object.__setattr__(
            self,
            "tolerance_mm",
            _non_negative(self.tolerance_mm, "probe tolerance_mm"),
        )


@dataclass(frozen=True)
class GeometryContract:
    """Expected measurable geometry for one already-exported mesh."""

    bounds_min: tuple[float, float, float]
    bounds_max: tuple[float, float, float]
    bounds_tolerance_mm: float
    volume_mm3: float | None = None
    volume_tolerance_mm3: float | None = None
    watertight: bool | None = None
    bounds_sufficient: bool = True
    surface_distance_probes: tuple[SurfaceDistanceProbe, ...] = ()

    def __post_init__(self) -> None:
        minimum = _xyz(self.bounds_min, "bounds_min")
        maximum = _xyz(self.bounds_max, "bounds_max")
        for axis, (low, high) in enumerate(zip(minimum, maximum)):
            if high < low:
                raise VerificationConfigError(
                    f"bounds_max[{axis}] may not be below bounds_min[{axis}]"
                )

        tolerance = _non_negative(
            self.bounds_tolerance_mm,
            "bounds_tolerance_mm",
        )

        volume = self.volume_mm3
        volume_tolerance = self.volume_tolerance_mm3
        if volume is not None:
            volume = _non_negative(volume, "volume_mm3")
            if volume_tolerance is None:
                raise VerificationConfigError(
                    "volume_tolerance_mm3 is required when volume_mm3 is set"
                )
            volume_tolerance = _non_negative(
                volume_tolerance,
                "volume_tolerance_mm3",
            )
        elif volume_tolerance is not None:
            raise VerificationConfigError(
                "volume_tolerance_mm3 requires volume_mm3"
            )

        if self.watertight is not None and not isinstance(
            self.watertight,
            bool,
        ):
            raise VerificationConfigError("watertight must be bool or None")
        if not isinstance(self.bounds_sufficient, bool):
            raise VerificationConfigError(
                "bounds_sufficient must be a bool"
            )

        probes = tuple(self.surface_distance_probes)
        for probe in probes:
            if not isinstance(probe, SurfaceDistanceProbe):
                raise VerificationConfigError(
                    "surface_distance_probes must contain SurfaceDistanceProbe"
                )
        labels = [probe.label for probe in probes]
        if len(set(labels)) != len(labels):
            raise VerificationConfigError(
                "surface-distance probe labels must be unique"
            )
        if (
            not self.bounds_sufficient
            and volume is None
            and not probes
        ):
            raise VerificationConfigError(
                "bounds_sufficient=False requires volume or surface probes"
            )

        object.__setattr__(self, "bounds_min", minimum)
        object.__setattr__(self, "bounds_max", maximum)
        object.__setattr__(self, "bounds_tolerance_mm", tolerance)
        object.__setattr__(self, "volume_mm3", volume)
        object.__setattr__(self, "volume_tolerance_mm3", volume_tolerance)
        object.__setattr__(self, "surface_distance_probes", probes)


def _load_mesh(path: Path) -> trimesh.Trimesh:
    """Load one measurable STL mesh."""

    path = Path(path)
    if not path.is_file():
        raise MeshLoadError(f"mesh file does not exist: {path}")
    if path.stat().st_size == 0:
        raise MeshLoadError(f"mesh file is empty: {path}")

    try:
        loaded = trimesh.load(path, process=False)
    except Exception as exc:
        raise MeshLoadError(f"could not load mesh: {path}: {exc}") from exc

    if isinstance(loaded, trimesh.Scene):
        parts = [
            geometry
            for geometry in loaded.geometry.values()
            if isinstance(geometry, trimesh.Trimesh)
            and len(geometry.vertices)
            and len(geometry.faces)
        ]
        if not parts:
            raise MeshLoadError(f"mesh contains no measurable geometry: {path}")
        loaded = trimesh.util.concatenate(parts)

    if not isinstance(loaded, trimesh.Trimesh):
        raise MeshLoadError(f"unsupported mesh object in: {path}")
    if len(loaded.vertices) == 0 or len(loaded.faces) == 0:
        raise MeshLoadError(f"mesh contains no measurable geometry: {path}")

    return loaded


def _list3(values: Any) -> list[float]:
    """Convert one numerical XYZ vector to stable JSON-compatible floats."""

    return [float(values[0]), float(values[1]), float(values[2])]


def _bounds_evidence(
    mesh: trimesh.Trimesh,
    contract: GeometryContract,
) -> dict[str, Any]:
    actual_min = _list3(mesh.bounds[0])
    actual_max = _list3(mesh.bounds[1])
    deltas = [
        abs(actual - expected)
        for actual, expected in zip(
            actual_min + actual_max,
            list(contract.bounds_min) + list(contract.bounds_max),
        )
    ]
    maximum_delta = max(deltas)
    passed = maximum_delta <= contract.bounds_tolerance_mm
    return {
        "expected_min": list(contract.bounds_min),
        "expected_max": list(contract.bounds_max),
        "actual_min": actual_min,
        "actual_max": actual_max,
        "max_delta_mm": float(maximum_delta),
        "tolerance_mm": contract.bounds_tolerance_mm,
        "pass": bool(passed),
    }


def _volume_evidence(
    mesh: trimesh.Trimesh,
    contract: GeometryContract,
) -> dict[str, Any]:
    assert contract.volume_mm3 is not None
    assert contract.volume_tolerance_mm3 is not None
    actual = abs(float(mesh.volume))
    delta = abs(actual - contract.volume_mm3)
    return {
        "expected_mm3": contract.volume_mm3,
        "actual_mm3": actual,
        "delta_mm3": delta,
        "tolerance_mm3": contract.volume_tolerance_mm3,
        "pass": bool(delta <= contract.volume_tolerance_mm3),
    }


def _watertight_evidence(
    mesh: trimesh.Trimesh,
    contract: GeometryContract,
) -> dict[str, Any]:
    assert contract.watertight is not None
    topology = mesh.copy()
    topology.process(validate=True)
    actual = bool(topology.is_watertight)
    return {
        "expected": contract.watertight,
        "actual": actual,
        "pass": actual is contract.watertight,
    }


def _probe_evidence(
    mesh: trimesh.Trimesh,
    probes: tuple[SurfaceDistanceProbe, ...],
) -> list[dict[str, Any]]:
    if not probes:
        return []

    points = [probe.point for probe in probes]
    try:
        _closest, distances, _triangle = trimesh.proximity.closest_point_naive(
            mesh,
            points,
        )
    except Exception as exc:
        raise MeshLoadError(
            f"could not measure mesh surface distances: {exc}"
        ) from exc

    result = []
    for probe, measured in zip(probes, distances):
        actual = float(measured)
        delta = abs(actual - probe.distance_mm)
        result.append(
            {
                "label": probe.label,
                "point": list(probe.point),
                "expected_mm": probe.distance_mm,
                "actual_mm": actual,
                "delta_mm": delta,
                "tolerance_mm": probe.tolerance_mm,
                "pass": bool(delta <= probe.tolerance_mm),
            }
        )
    return result


def validate_mesh_geometry(
    mesh_path: Path,
    contract: GeometryContract,
) -> dict[str, Any]:
    """Validate one exported mesh and return deterministic structured evidence."""

    if not isinstance(contract, GeometryContract):
        raise VerificationConfigError(
            "contract must be a GeometryContract"
        )

    mesh = _load_mesh(Path(mesh_path))
    evidence: dict[str, Any] = {}

    bounds = _bounds_evidence(mesh, contract)
    evidence["bounds"] = bounds
    failed = not bounds["pass"]

    if contract.volume_mm3 is not None:
        volume = _volume_evidence(mesh, contract)
        evidence["volume"] = volume
        failed = failed or not volume["pass"]

    if contract.watertight is not None:
        watertight = _watertight_evidence(mesh, contract)
        evidence["watertight"] = watertight
        failed = failed or not watertight["pass"]

    if contract.surface_distance_probes:
        probes = _probe_evidence(mesh, contract.surface_distance_probes)
        evidence["surface_distance_probes"] = probes
        failed = failed or any(not probe["pass"] for probe in probes)

    if failed:
        raise VerificationFailure(
            "mesh geometry does not satisfy the contract",
            evidence=evidence,
        )

    return evidence
