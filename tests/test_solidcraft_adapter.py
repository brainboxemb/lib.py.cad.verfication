"""Requirement tests for the SolidCraft CAD-tool verification adapter."""

from __future__ import annotations

import inspect
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cad_verification import (
    BodyEnvelope,
    SolidCraftBodyExpectation,
    SolidCraftEvidenceError,
    SolidCraftModelExpectation,
    SolidCraftSketchExpectation,
    SolidCraftTimelineExpectation,
    VerificationFailure,
    evaluate_solidcraft_model,
    inspect_solidcraft_model,
    mutate_solidcraft_model,
    verify_solidcraft_measurements,
)
import cad_verification.adapters.solidcraft as solidcraft_module


class SolidCraftAdapterTests(unittest.TestCase):
    def measurements(self):
        return {
            "body_count": 1,
            "bodies": [
                {
                    "name": "Plate",
                    "bbox": {
                        "min": [-20.0, -15.0, 0.0],
                        "max": [20.0, 15.0, 10.0],
                    },
                    "volume_mm3": 12000.0,
                    "sheet_metal": False,
                    "closed": True,
                }
            ],
            "params": [
                {"name": "length", "value": 40.0},
                {"name": "width", "value": 30.0},
                {"name": "height", "value": 10.0},
            ],
            "timeline": [
                {
                    "type": "BoxFeature",
                    "name": "Base",
                    "error": None,
                    "warning": None,
                }
            ],
            "sketches": [
                {
                    "name": "Profile",
                    "profiles": 1,
                    "curves": 4,
                    "status": "solved",
                }
            ],
        }

    def expectation(self):
        return SolidCraftModelExpectation(
            body_count=1,
            body_envelopes=(
                BodyEnvelope(
                    (-20.0, -15.0, 0.0),
                    (20.0, 15.0, 10.0),
                    "plate",
                ),
            ),
            bounds_tolerance=0.001,
            parameters={
                "length": 40.0,
                "width": 30.0,
                "height": 10.0,
            },
            named_bodies=(
                SolidCraftBodyExpectation(
                    name_prefix="Plate",
                    minimum=(-20.0, -15.0, 0.0),
                    maximum=(20.0, 15.0, 10.0),
                    bounds_tolerance=0.001,
                    volume_mm3=12000.0,
                    volume_tolerance=0.01,
                    sheet_metal=False,
                    closed=True,
                ),
            ),
            timeline=(
                SolidCraftTimelineExpectation(
                    feature_type="BoxFeature",
                    name="Base",
                    error=None,
                    warning=None,
                ),
            ),
            sketches=(
                SolidCraftSketchExpectation(
                    name="Profile",
                    profiles=1,
                    curves=4,
                    status="solved",
                ),
            ),
        )

    def test_model_expectation_verifies_solidcraft_measurements(self):
        evidence = verify_solidcraft_measurements(
            self.measurements(),
            self.expectation(),
        )

        self.assertEqual(
            list(evidence),
            [
                "body_count",
                "body_envelopes",
                "parameters",
                "named_bodies",
                "timeline",
                "sketches",
            ],
        )
        self.assertTrue(evidence["body_count"]["pass"])
        self.assertTrue(evidence["body_envelopes"]["pass"])
        self.assertTrue(evidence["parameters"]["pass"])
        self.assertTrue(evidence["named_bodies"][0]["volume"]["pass"])
        self.assertTrue(evidence["timeline"]["pass"])
        self.assertTrue(evidence["sketches"][0]["pass"])

    def test_model_mismatch_is_verification_failure(self):
        data = self.measurements()
        data["params"][0]["value"] = 41.0

        with self.assertRaises(VerificationFailure):
            verify_solidcraft_measurements(data, self.expectation())

    def test_malformed_body_is_evidence_error_and_is_not_skipped(self):
        data = self.measurements()
        data["bodies"].append({"name": "Broken", "bbox": None})
        data["body_count"] = 2

        expectation = SolidCraftModelExpectation(
            body_count=2,
            body_envelopes=(
                BodyEnvelope(
                    (-20.0, -15.0, 0.0),
                    (20.0, 15.0, 10.0),
                ),
                BodyEnvelope((0, 0, 0), (1, 1, 1)),
            ),
            bounds_tolerance=0.001,
        )

        with self.assertRaisesRegex(
            SolidCraftEvidenceError,
            r"bodies\[1\]\.bbox",
        ):
            verify_solidcraft_measurements(data, expectation)

    def test_malformed_parameter_row_is_evidence_error(self):
        data = self.measurements()
        data["params"][0] = {"name": "length", "value": "forty"}

        with self.assertRaisesRegex(SolidCraftEvidenceError, r"params\[0\]"):
            verify_solidcraft_measurements(
                data,
                SolidCraftModelExpectation(parameters={"length": 40.0}),
            )

    def test_named_body_must_match_exactly_once(self):
        data = self.measurements()
        duplicate = dict(data["bodies"][0])
        duplicate["name"] = "Plate copy"
        data["bodies"].append(duplicate)
        data["body_count"] = 2

        expectation = SolidCraftModelExpectation(
            named_bodies=(
                SolidCraftBodyExpectation(name_prefix="Plate"),
            )
        )

        with self.assertRaises(VerificationFailure):
            verify_solidcraft_measurements(data, expectation)

    def test_evaluate_command_and_json_loading(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model = root / "model.sc"
            destination = root / "measurements.json"
            destination.write_text(
                json.dumps(self.measurements()),
                encoding="utf-8",
            )

            with patch.object(solidcraft_module, "run_command") as run:
                result = evaluate_solidcraft_model(model, destination)

            run.assert_called_once_with(
                [
                    "solidcraft-cli",
                    "eval",
                    str(model),
                    "--json-out",
                    str(destination),
                ]
            )
            self.assertEqual(result["body_count"], 1)

    def test_mutate_command_is_exact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model = root / "model.sc"
            command = root / "change.json"
            destination = root / "changed.sc"

            with patch.object(solidcraft_module, "run_command") as run:
                mutate_solidcraft_model(model, command, destination)

            run.assert_called_once_with(
                [
                    "solidcraft-cli",
                    "run",
                    str(command),
                    "--in",
                    str(model),
                    "--param-check",
                    "strict",
                    "--save",
                    str(destination),
                ]
            )

    def test_inspection_command_and_json_loading(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            model = root / "model.sc"
            command = root / "inspect.json"
            destination = root / "inspection.json"
            destination.write_text(
                json.dumps([{"flat_size_mm": [80, 40, 2]}]),
                encoding="utf-8",
            )

            with patch.object(solidcraft_module, "run_command") as run:
                result = inspect_solidcraft_model(
                    model,
                    command,
                    destination,
                )

            run.assert_called_once_with(
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
                    str(destination),
                ]
            )
            self.assertEqual(result[0]["flat_size_mm"], [80, 40, 2])

    def test_invalid_json_is_solidcraft_evidence_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            destination = Path(tmp) / "measurements.json"
            destination.write_text("{broken", encoding="utf-8")

            with patch.object(solidcraft_module, "run_command"):
                with self.assertRaises(SolidCraftEvidenceError):
                    evaluate_solidcraft_model(
                        Path(tmp) / "model.sc",
                        destination,
                    )

    def test_adapter_has_no_forge_or_ci_dependency(self):
        source = inspect.getsource(solidcraft_module).lower()
        forbidden_imports = (
            "import scpf",
            "from scpf",
            "import scons",
            "from scons",
            "cad_ci",
            "tool.cad.ci",
        )
        for value in forbidden_imports:
            with self.subTest(value=value):
                self.assertNotIn(value, source)


if __name__ == "__main__":
    unittest.main()
