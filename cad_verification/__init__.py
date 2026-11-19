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
from .verification import verify

__all__ = [
    "ArtifactError",
    "BodyEnvelope",
    "CheckOutcome",
    "CommandError",
    "CommandFailed",
    "CommandResult",
    "CommandTimedOut",
    "GeometryContract",
    "MeshLoadError",
    "VerificationCheck",
    "VerificationConfigError",
    "VerificationContext",
    "VerificationError",
    "VerificationFailure",
    "SurfaceDistanceProbe",
    "compare_bounds",
    "compare_scalar",
    "compare_vector",
    "match_body_envelopes",
    "run_command",
    "validate_mesh_geometry",
    "verify",
]
