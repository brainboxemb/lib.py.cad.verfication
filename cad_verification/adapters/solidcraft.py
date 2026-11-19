"""SolidCraft-specific verification adapter.

The adapter understands SolidCraft result schemas and command-line inspection
operations. Model-specific expected values remain consumer-supplied data.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
import math
from numbers import Real
from pathlib import Path
from typing import Any, Mapping

from ..assertions import require_equal
from ..comparison import (
    BodyEnvelope,
    compare_bounds,
    compare_scalar,
    match_body_envelopes,
)
from ..errors import (
    SolidCraftEvidenceError,
    VerificationConfigError,
)
from ..process import run_command


def _config_number(value: Any, name: str) -> float:
    """Return one finite numeric expectation value."""

    if isinstance(value, bool) or not isinstance(value, Real):
        raise VerificationConfigError(f"{name} must be a number")
    result = float(value)
    if not math.isfinite(result):
        raise VerificationConfigError(f"{name} must be finite")
    return result


def _config_tolerance(value: Any, name: str) -> float:
    """Return one finite non-negative expectation tolerance."""

    result = _config_number(value, name)
    if result < 0:
        raise VerificationConfigError(f"{name} may not be negative")
    return result


def _config_text(value: Any, name: str) -> str:
    """Return one non-empty string from adapter configuration."""

    if not isinstance(value, str):
        raise VerificationConfigError(f"{name} must be a string")
    result = value.strip()
    if not result:
        raise VerificationConfigError(f"{name} may not be empty")
    return result


def _config_optional_text(value: Any, name: str) -> str | None:
    """Return one optional string from adapter configuration."""

    if value is None:
        return None
    if not isinstance(value, str):
        raise VerificationConfigError(f"{name} must be a string or None")
    return value


def _config_count(value: Any, name: str) -> int:
    """Return one non-negative integer expectation."""

    if isinstance(value, bool) or not isinstance(value, int):
        raise VerificationConfigError(f"{name} must be an integer")
    if value < 0:
        raise VerificationConfigError(f"{name} may not be negative")
    return value


def _evidence_mapping(value: Any, path: str) -> Mapping[str, Any]:
    """Return one SolidCraft object or raise a schema error."""

    if not isinstance(value, Mapping):
        raise SolidCraftEvidenceError(f"{path} must be an object")
    return value


def _evidence_list(value: Any, path: str) -> list[Any]:
    """Return one SolidCraft array or raise a schema error."""

    if not isinstance(value, list):
        raise SolidCraftEvidenceError(f"{path} must be an array")
    return value


def _evidence_number(value: Any, path: str) -> float:
    """Return one finite SolidCraft numeric value."""

    if isinstance(value, bool) or not isinstance(value, Real):
        raise SolidCraftEvidenceError(f"{path} must be a number")
    result = float(value)
    if not math.isfinite(result):
        raise SolidCraftEvidenceError(f"{path} must be finite")
    return result


def _evidence_bool(value: Any, path: str) -> bool:
    """Return one literal SolidCraft boolean value."""

    if not isinstance(value, bool):
        raise SolidCraftEvidenceError(f"{path} must be a boolean")
    return value


def _evidence_text(value: Any, path: str) -> str:
    """Return one non-empty SolidCraft text value."""

    if not isinstance(value, str):
        raise SolidCraftEvidenceError(f"{path} must be a string")
    result = value.strip()
    if not result:
        raise SolidCraftEvidenceError(f"{path} may not be empty")
    return result


def _evidence_optional_text(value: Any, path: str) -> str | None:
    """Return one optional SolidCraft text value."""

    if value is None:
        return None
    if not isinstance(value, str):
        raise SolidCraftEvidenceError(f"{path} must be a string or null")
    return value


@dataclass(frozen=True)
class SolidCraftBodyExpectation:
    """Model-specific expectations for exactly one named SolidCraft body."""

    name_prefix: str
    minimum: tuple[float, float, float] | None = None
    maximum: tuple[float, float, float] | None = None
    bounds_tolerance: float = 0.0
    volume_mm3: float | None = None
    volume_tolerance: float = 0.0
    sheet_metal: bool | None = None
    closed: bool | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "name_prefix",
            _config_text(self.name_prefix, "name_prefix"),
        )
        if (self.minimum is None) != (self.maximum is None):
            raise VerificationConfigError(
                "minimum and maximum must be supplied together"
            )
        if self.minimum is not None and self.maximum is not None:
            envelope = BodyEnvelope(self.minimum, self.maximum)
            object.__setattr__(self, "minimum", envelope.minimum)
            object.__setattr__(self, "maximum", envelope.maximum)

        object.__setattr__(
            self,
            "bounds_tolerance",
            _config_tolerance(self.bounds_tolerance, "bounds_tolerance"),
        )

        if self.volume_mm3 is not None:
            object.__setattr__(
                self,
                "volume_mm3",
                _config_number(self.volume_mm3, "volume_mm3"),
            )
        object.__setattr__(
            self,
            "volume_tolerance",
            _config_tolerance(self.volume_tolerance, "volume_tolerance"),
        )

        for name in ("sheet_metal", "closed"):
            value = getattr(self, name)
            if value is not None and not isinstance(value, bool):
                raise VerificationConfigError(
                    f"{name} must be a boolean or None"
                )


@dataclass(frozen=True)
class SolidCraftTimelineExpectation:
    """One expected SolidCraft timeline row."""

    feature_type: str
    name: str | None = None
    error: str | None = None
    warning: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "feature_type",
            _config_text(self.feature_type, "feature_type"),
        )
        for field_name in ("name", "error", "warning"):
            object.__setattr__(
                self,
                field_name,
                _config_optional_text(
                    getattr(self, field_name),
                    field_name,
                ),
            )

    def evidence(self) -> dict[str, Any]:
        """Return the expected row in SolidCraft-neutral evidence shape."""

        return {
            "type": self.feature_type,
            "name": self.name,
            "error": self.error,
            "warning": self.warning,
        }


@dataclass(frozen=True)
class SolidCraftSketchExpectation:
    """One expected SolidCraft sketch summary."""

    name: str
    profiles: int
    curves: int
    status: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", _config_text(self.name, "name"))
        object.__setattr__(
            self,
            "profiles",
            _config_count(self.profiles, "profiles"),
        )
        object.__setattr__(
            self,
            "curves",
            _config_count(self.curves, "curves"),
        )
        object.__setattr__(
            self,
            "status",
            _config_text(self.status, "status"),
        )

    def evidence(self) -> dict[str, Any]:
        """Return deterministic expected sketch evidence."""

        return {
            "name": self.name,
            "profiles": self.profiles,
            "curves": self.curves,
            "status": self.status,
        }


@dataclass(frozen=True)
class SolidCraftModelExpectation:
    """Model-specific data consumed by the SolidCraft verification adapter."""

    body_count: int | None = None
    body_envelopes: tuple[BodyEnvelope, ...] | None = None
    bounds_tolerance: float = 0.0
    parameters: Mapping[str, float] | None = None
    named_bodies: tuple[SolidCraftBodyExpectation, ...] = ()
    timeline: tuple[SolidCraftTimelineExpectation, ...] | None = None
    sketches: tuple[SolidCraftSketchExpectation, ...] = ()

    def __post_init__(self) -> None:
        if self.body_count is not None:
            object.__setattr__(
                self,
                "body_count",
                _config_count(self.body_count, "body_count"),
            )

        if self.body_envelopes is not None:
            envelopes = tuple(self.body_envelopes)
            if not all(isinstance(item, BodyEnvelope) for item in envelopes):
                raise VerificationConfigError(
                    "body_envelopes must contain BodyEnvelope values"
                )
            object.__setattr__(self, "body_envelopes", envelopes)

        object.__setattr__(
            self,
            "bounds_tolerance",
            _config_tolerance(self.bounds_tolerance, "bounds_tolerance"),
        )

        if self.parameters is not None:
            if not isinstance(self.parameters, Mapping):
                raise VerificationConfigError("parameters must be a mapping")
            normalized_parameters: dict[str, float] = {}
            for key, value in self.parameters.items():
                name = _config_text(key, "parameter name")
                if name in normalized_parameters:
                    raise VerificationConfigError(
                        f"duplicate parameter expectation: {name}"
                    )
                normalized_parameters[name] = _config_number(
                    value,
                    f"parameter {name}",
                )
            object.__setattr__(
                self,
                "parameters",
                dict(sorted(normalized_parameters.items())),
            )

        named_bodies = tuple(self.named_bodies)
        if not all(
            isinstance(item, SolidCraftBodyExpectation)
            for item in named_bodies
        ):
            raise VerificationConfigError(
                "named_bodies must contain SolidCraftBodyExpectation values"
            )
        object.__setattr__(self, "named_bodies", named_bodies)

        if self.timeline is not None:
            timeline = tuple(self.timeline)
            if not all(
                isinstance(item, SolidCraftTimelineExpectation)
                for item in timeline
            ):
                raise VerificationConfigError(
                    "timeline must contain SolidCraftTimelineExpectation values"
                )
            object.__setattr__(self, "timeline", timeline)

        sketches = tuple(self.sketches)
        if not all(
            isinstance(item, SolidCraftSketchExpectation)
            for item in sketches
        ):
            raise VerificationConfigError(
                "sketches must contain SolidCraftSketchExpectation values"
            )
        object.__setattr__(self, "sketches", sketches)

        if (
            self.body_count is None
            and self.body_envelopes is None
            and self.parameters is None
            and not self.named_bodies
            and self.timeline is None
            and not self.sketches
        ):
            raise VerificationConfigError(
                "SolidCraftModelExpectation must request at least one check"
            )


def _load_json(path: Path, *, object_required: bool) -> Any:
    """Load one SolidCraft JSON evidence file."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SolidCraftEvidenceError(
            f"could not read SolidCraft JSON evidence: {path}"
        ) from exc

    if object_required and not isinstance(value, Mapping):
        raise SolidCraftEvidenceError(
            f"SolidCraft evidence must contain one object: {path}"
        )
    if not object_required and not isinstance(value, (Mapping, list)):
        raise SolidCraftEvidenceError(
            f"SolidCraft inspection evidence must be an object or array: {path}"
        )
    return value


def evaluate_solidcraft_model(
    model_path: Path,
    destination: Path,
) -> dict[str, Any]:
    """Evaluate one saved SolidCraft model and load its measurement object."""

    model = Path(model_path)
    output = Path(destination)
    run_command(
        [
            "solidcraft-cli",
            "eval",
            str(model),
            "--json-out",
            str(output),
        ]
    )
    value = _load_json(output, object_required=True)
    return dict(value)


def mutate_solidcraft_model(
    model_path: Path,
    command_path: Path,
    destination: Path,
) -> Path:
    """Apply one SolidCraft command document to an existing saved model."""

    model = Path(model_path)
    command = Path(command_path)
    output = Path(destination)
    run_command(
        [
            "solidcraft-cli",
            "run",
            str(command),
            "--in",
            str(model),
            "--param-check",
            "strict",
            "--save",
            str(output),
        ]
    )
    return output


def inspect_solidcraft_model(
    model_path: Path,
    command_path: Path,
    destination: Path,
) -> Any:
    """Execute one read-only SolidCraft inspection and load its JSON result."""

    model = Path(model_path)
    command = Path(command_path)
    output = Path(destination)
    run_command(
        [
            "solidcraft-cli",
            "run",
            str(command),
            "--in",
            str(model),
            "--param-check",
            "strict",
            "--results",
            "--json-out",
            str(output),
        ]
    )
    return _load_json(output, object_required=False)


def _body_rows(measurements: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    """Return validated SolidCraft body rows without skipping malformed rows."""

    if "bodies" not in measurements:
        raise SolidCraftEvidenceError("bodies is required")
    values = _evidence_list(measurements["bodies"], "bodies")
    result = []
    for index, value in enumerate(values):
        result.append(_evidence_mapping(value, f"bodies[{index}]"))
    return result


def _body_name(body: Mapping[str, Any], path: str) -> str:
    """Return one validated SolidCraft body name."""

    if "name" not in body:
        raise SolidCraftEvidenceError(f"{path}.name is required")
    return _evidence_text(body["name"], f"{path}.name")


def _body_envelope(
    body: Mapping[str, Any],
    path: str,
) -> BodyEnvelope:
    """Convert one SolidCraft body row to a generic body envelope."""

    if "bbox" not in body:
        raise SolidCraftEvidenceError(f"{path}.bbox is required")
    bbox = _evidence_mapping(body["bbox"], f"{path}.bbox")
    if "min" not in bbox or "max" not in bbox:
        raise SolidCraftEvidenceError(
            f"{path}.bbox must contain min and max"
        )

    label = None
    if "name" in body:
        raw_name = body["name"]
        if raw_name is not None:
            label = _evidence_text(raw_name, f"{path}.name")

    try:
        return BodyEnvelope(
            tuple(bbox["min"]),
            tuple(bbox["max"]),
            label=label,
        )
    except (TypeError, VerificationConfigError) as exc:
        raise SolidCraftEvidenceError(
            f"{path}.bbox is not a valid XYZ envelope"
        ) from exc


def _parameters(measurements: Mapping[str, Any]) -> dict[str, float]:
    """Normalize SolidCraft parameter rows to a stable name/value mapping."""

    if "params" not in measurements:
        raise SolidCraftEvidenceError("params is required")
    rows = _evidence_list(measurements["params"], "params")
    result: dict[str, float] = {}
    for index, value in enumerate(rows):
        path = f"params[{index}]"
        row = _evidence_mapping(value, path)
        if "name" not in row or "value" not in row:
            raise SolidCraftEvidenceError(
                f"{path} must contain name and value"
            )
        name = _evidence_text(row["name"], f"{path}.name")
        if name in result:
            raise SolidCraftEvidenceError(
                f"duplicate SolidCraft parameter: {name}"
            )
        result[name] = _evidence_number(row["value"], f"{path}.value")
    return dict(sorted(result.items()))


def _timeline_rows(
    measurements: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Normalize the SolidCraft timeline schema used by expectations."""

    if "timeline" not in measurements:
        raise SolidCraftEvidenceError("timeline is required")
    rows = _evidence_list(measurements["timeline"], "timeline")
    result = []
    for index, value in enumerate(rows):
        path = f"timeline[{index}]"
        row = _evidence_mapping(value, path)
        if "type" not in row:
            raise SolidCraftEvidenceError(f"{path}.type is required")
        result.append(
            {
                "type": _evidence_text(row["type"], f"{path}.type"),
                "name": _evidence_optional_text(
                    row.get("name"),
                    f"{path}.name",
                ),
                "error": _evidence_optional_text(
                    row.get("error"),
                    f"{path}.error",
                ),
                "warning": _evidence_optional_text(
                    row.get("warning"),
                    f"{path}.warning",
                ),
            }
        )
    return result


def _sketch_rows(
    measurements: Mapping[str, Any],
) -> list[Mapping[str, Any]]:
    """Return validated SolidCraft sketch rows."""

    if "sketches" not in measurements:
        raise SolidCraftEvidenceError("sketches is required")
    rows = _evidence_list(measurements["sketches"], "sketches")
    return [
        _evidence_mapping(value, f"sketches[{index}]")
        for index, value in enumerate(rows)
    ]


def _actual_count(value: Any, path: str) -> int:
    """Return one non-negative integer from SolidCraft evidence."""

    if isinstance(value, bool) or not isinstance(value, int):
        raise SolidCraftEvidenceError(f"{path} must be an integer")
    if value < 0:
        raise SolidCraftEvidenceError(f"{path} may not be negative")
    return value


def verify_solidcraft_measurements(
    measurements: Mapping[str, Any],
    expectation: SolidCraftModelExpectation,
) -> dict[str, Any]:
    """Apply model-specific expectation data to SolidCraft measurements."""

    if not isinstance(measurements, Mapping):
        raise SolidCraftEvidenceError(
            "SolidCraft measurements must be an object"
        )
    if not isinstance(expectation, SolidCraftModelExpectation):
        raise VerificationConfigError(
            "expectation must be a SolidCraftModelExpectation"
        )

    evidence: dict[str, Any] = {}
    bodies: list[Mapping[str, Any]] | None = None

    def body_rows() -> list[Mapping[str, Any]]:
        nonlocal bodies
        if bodies is None:
            bodies = _body_rows(measurements)
        return bodies

    if expectation.body_count is not None:
        if "body_count" not in measurements:
            raise SolidCraftEvidenceError("body_count is required")
        actual_count = _actual_count(
            measurements["body_count"],
            "body_count",
        )
        evidence["body_count"] = require_equal(
            expectation.body_count,
            actual_count,
            label="SolidCraft body count",
        )

    if expectation.body_envelopes is not None:
        actual_envelopes = tuple(
            _body_envelope(row, f"bodies[{index}]")
            for index, row in enumerate(body_rows())
        )
        evidence["body_envelopes"] = match_body_envelopes(
            expectation.body_envelopes,
            actual_envelopes,
            expectation.bounds_tolerance,
        )

    if expectation.parameters is not None:
        evidence["parameters"] = require_equal(
            dict(expectation.parameters),
            _parameters(measurements),
            label="SolidCraft parameters",
        )

    if expectation.named_bodies:
        named_evidence = []
        rows = body_rows()
        names = [
            _body_name(row, f"bodies[{index}]")
            for index, row in enumerate(rows)
        ]
        for expected in expectation.named_bodies:
            matches = [
                (index, row, names[index])
                for index, row in enumerate(rows)
                if names[index].startswith(expected.name_prefix)
            ]
            require_equal(
                1,
                len(matches),
                label=f"{expected.name_prefix} body count",
            )
            index, body, body_name = matches[0]
            path = f"bodies[{index}]"
            item_evidence: dict[str, Any] = {
                "name_prefix": expected.name_prefix,
                "body_name": body_name,
            }

            if expected.minimum is not None and expected.maximum is not None:
                actual = _body_envelope(body, path)
                item_evidence["bounds"] = compare_bounds(
                    expected.minimum,
                    expected.maximum,
                    actual.minimum,
                    actual.maximum,
                    expected.bounds_tolerance,
                    label=f"{expected.name_prefix} bounds",
                )

            if expected.volume_mm3 is not None:
                if "volume_mm3" not in body:
                    raise SolidCraftEvidenceError(
                        f"{path}.volume_mm3 is required"
                    )
                item_evidence["volume"] = compare_scalar(
                    expected.volume_mm3,
                    _evidence_number(
                        body["volume_mm3"],
                        f"{path}.volume_mm3",
                    ),
                    expected.volume_tolerance,
                    label=f"{expected.name_prefix} volume",
                )

            if expected.sheet_metal is not None:
                if "sheet_metal" not in body:
                    raise SolidCraftEvidenceError(
                        f"{path}.sheet_metal is required"
                    )
                item_evidence["sheet_metal"] = require_equal(
                    expected.sheet_metal,
                    _evidence_bool(
                        body["sheet_metal"],
                        f"{path}.sheet_metal",
                    ),
                    label=f"{expected.name_prefix} sheet_metal",
                )

            if expected.closed is not None:
                if "closed" not in body:
                    raise SolidCraftEvidenceError(
                        f"{path}.closed is required"
                    )
                item_evidence["closed"] = require_equal(
                    expected.closed,
                    _evidence_bool(body["closed"], f"{path}.closed"),
                    label=f"{expected.name_prefix} closed",
                )

            named_evidence.append(item_evidence)
        evidence["named_bodies"] = named_evidence

    if expectation.timeline is not None:
        expected_timeline = [
            item.evidence()
            for item in expectation.timeline
        ]
        evidence["timeline"] = require_equal(
            expected_timeline,
            _timeline_rows(measurements),
            label="SolidCraft timeline",
        )

    if expectation.sketches:
        rows = _sketch_rows(measurements)
        normalized_names = []
        for index, row in enumerate(rows):
            if "name" not in row:
                raise SolidCraftEvidenceError(
                    f"sketches[{index}].name is required"
                )
            normalized_names.append(
                _evidence_text(row["name"], f"sketches[{index}].name")
            )

        sketch_evidence = []
        for expected in expectation.sketches:
            matches = [
                (index, row)
                for index, row in enumerate(rows)
                if normalized_names[index] == expected.name
            ]
            require_equal(
                1,
                len(matches),
                label=f"{expected.name} sketch count",
            )
            index, row = matches[0]
            path = f"sketches[{index}]"

            for field_name in ("profiles", "curves", "status"):
                if field_name not in row:
                    raise SolidCraftEvidenceError(
                        f"{path}.{field_name} is required"
                    )

            actual = {
                "name": expected.name,
                "profiles": _actual_count(
                    row["profiles"],
                    f"{path}.profiles",
                ),
                "curves": _actual_count(
                    row["curves"],
                    f"{path}.curves",
                ),
                "status": _evidence_text(
                    row["status"],
                    f"{path}.status",
                ),
            }
            sketch_evidence.append(
                require_equal(
                    expected.evidence(),
                    actual,
                    label=f"{expected.name} sketch",
                )
            )
        evidence["sketches"] = sketch_evidence

    return evidence
