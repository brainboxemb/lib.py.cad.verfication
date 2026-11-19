"""Reusable CAD/model verification library."""

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
    "run_command",
    "validate_mesh_geometry",
    "verify",
]
