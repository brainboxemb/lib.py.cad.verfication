"""Reusable CAD/model verification library."""

from .comparison import (
    BodyEnvelope,
    compare_bounds,
    compare_scalar,
    compare_vector,
    match_body_envelopes,
)
from .errors import (
    ArtifactError,
    CommandError,
    CommandFailed,
    CommandTimedOut,
    MeshLoadError,
    VerificationConfigError,
    VerificationError,
    VerificationFailure,
    VisualEvidenceError,
)
from .geometry import (
    GeometryContract,
    SurfaceDistanceProbe,
    validate_mesh_geometry,
)
from .model import (
    CheckOutcome,
    CommandResult,
    VerificationCheck,
    VerificationContext,
)
from .process import run_command
from .visual import (
    ExpectedBox,
    OrthographicCamera,
    ThroughHole,
    ThroughSlot,
    VisualViewEvidence,
    compare_images,
    decode_baseline,
    draw_expected_geometry,
    encode_baseline,
    make_goal_image,
    make_overlay_image,
    normalize_image,
    project_points,
    write_diff_image,
)
from .verification import verify

__all__ = [
    "ArtifactError",
    "BodyEnvelope",
    "CheckOutcome",
    "CommandError",
    "CommandFailed",
    "CommandResult",
    "CommandTimedOut",
    "ExpectedBox",
    "GeometryContract",
    "OrthographicCamera",
    "MeshLoadError",
    "VerificationCheck",
    "VerificationConfigError",
    "VerificationContext",
    "VerificationError",
    "VerificationFailure",
    "SurfaceDistanceProbe",
    "ThroughHole",
    "ThroughSlot",
    "VisualEvidenceError",
    "VisualViewEvidence",
    "compare_bounds",
    "compare_images",
    "compare_scalar",
    "compare_vector",
    "decode_baseline",
    "draw_expected_geometry",
    "encode_baseline",
    "make_goal_image",
    "make_overlay_image",
    "match_body_envelopes",
    "normalize_image",
    "project_points",
    "run_command",
    "validate_mesh_geometry",
    "verify",
    "write_diff_image",
]
